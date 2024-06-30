from .....cores.implement.egress import Core

from attrs import define, field
from typing import Any, Iterable, NoReturn, Tuple, Union
from pathlib import Path

from logging import Logger
import sqlite3

@define(kw_only=True)
class Sqlite3EgressCore(Core):
    # Core Configs
    input: Union[Iterable, Any] = field(default=None, )
    heartbeat: int = field(default=1, )
    forgiving: bool = field(default=False, )
    backpressure: int = field(default=0)
    on_error: callable = field(default=None)
    logger:Logger = field(default=None)
    
    # DB Configs
    db_path: Union[Path , str] = field(init=True)
    isolation_level: str = field(default='IMMEDIATE')
    timeout: int = field(default=10800)
    
    # Egress Configs
    table_name: str = field(init=True)
    ensure_table: bool = field(default=True)
    columns_mapping:dict = field(default=None)
    upsert:bool = field(default=True)
    batch_mode: bool = field(default=False)
    skip_nulls:bool = field(default=True)
    
    # TODO: Created interface/ABC called DelayedInit / or DelayInput whatever
    def __call__(self, input:Union[Iterable, Any]) -> Any:
        self.input = input
        return self
    
    def constructor(self) -> NoReturn:
        self.connection = sqlite3.connect(database=self.db_path,
                                          isolation_level=self.isolation_level,
                                          timeout=self.timeout)
        self.cursor = self.connection.cursor()
        
        if self.ensure_table:
            if self.columns_mapping == None:
                raise AttributeError("Can't ensure table if no columns mapping provided.")
            
            column_definitions = ', '.join([f"{column_name} {column_type}" 
                                            for column_name, column_type 
                                            in self.columns_mapping.items()])
        
            create_statement = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({column_definitions});"
            
            self.cursor.execute(create_statement)
            self.connection.commit()
        
        # Init vars
        self.total_loaded = 0
        
        return self

    def destructor(self, exc_type, exc_value, traceback) -> NoReturn:
        if self.logger:
            verb = "Upserted" if self.upsert else "Appended"
            self.logger.debug(f"{verb} {self.total_loaded} records into '{self.table_name}' in '{self.db_path}'.")
        
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if self.connection:
            self.connection.commit()
            self.connection.close()
            self.connection = None
    
    def callback(self, record: Any, exception: Exception) -> NoReturn:
        if exception is None:
            if self.batch_mode:
                self.total_loaded += len(record)
            else: 
                self.total_loaded += 1
        else:
            if self.on_error is not None:
                self.on_error(record, exception)
            
    def pulse(self) -> NoReturn:
        self.connection.commit()
    
    def consume(self, record: Any) -> NoReturn:
        if self.skip_nulls == True and record == None:
            return
        
        insert_query = "INSERT" if not self.upsert else "INSERT OR REPLACE"
        insert_query += " INTO " + self.table_name + " VALUES ({})"
        
        if self.batch_mode:
            self.cursor.executemany(insert_query, record)
            self.connection.commit()
        else:
            if not isinstance(record, Tuple):
                record = (record, )
                
            placeholders = ','.join(['?'] * len(record))
            
            # Construct the INSERT query with dynamic placeholders
            self.cursor.execute(insert_query.format(placeholders), record)