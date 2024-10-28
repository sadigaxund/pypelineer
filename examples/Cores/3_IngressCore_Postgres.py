'''
    www.youtube.com/@Pypelineer
'''

from pypelineer.cores import IngressCore, IngressType

import psycopg as pg
import dotenv as env
import os

# Load environment variables
env.load_dotenv()

PG_PARAMS = {
    "host":     os.getenv("POSTGRES_HOST"),
    "port":     os.getenv("POSTGRES_PORT"),
    "dbname":   os.getenv("POSTGRES_NAME"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASS")
}

'''
    www.youtube.com/@Pypelineer
'''

SELECT_QUERY = 'SELECT * FROM employees ORDER BY id ASC'

class ReadFromPostgres_v1(IngressCore, Type=IngressType.INPUT):
    def constructor(self):
        connection: pg.Connection = None 
        cursor: pg.Cursor = None
        
        try:
            connection = pg.connect(**PG_PARAMS)
            cursor = connection.cursor()
            
            # Extract all results and save to input:
            cursor.execute(SELECT_QUERY)
            self.input = cursor.fetchall()
            
        except:
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
    def destructor(self, exc_type, exc_value, traceback):
        pass
    
    def produce(self):
        return next(self.input)

class ReadFromPostgres_v2(IngressCore, Type=IngressType.FUNCTION):
    def constructor(self):
        self.connection: pg.Connection = pg.connect(**PG_PARAMS) 
        self.cursor: pg.Cursor = self.connection.cursor() 
        self.cursor.execute(SELECT_QUERY)
        
    def destructor(self, exc_type, exc_value, traceback):
        # Destroy cursor if it was ever created
        if self.cursor is not None:
            self.cursor.close()
            
        # Close connection if it was ever opened
        if self.connection is not None:
            # Any Exception caught during execution
            if exc_type is not None:
                # Discard all changes
                self.connection.rollback()
            else:
                # Save all changes
                self.connection.commit()
            # Close
            self.connection.close()

    def available(self):
        return self.cursor.rownumber < self.cursor.rowcount
    
    def iterate(self):
        pass
    
    def produce(self):
        # Load result one by one
        result = self.cursor.fetchone()
        
        # Return something more complex
        column_names = [column._name for column in self.cursor.description]
        return dict(zip(column_names, result))

if __name__ == '__main__':
    with ReadFromPostgres_v2() as employees:
        for employee in employees:
            print(employee)

