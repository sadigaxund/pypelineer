from typing import Any, Iterable, NoReturn
from pypelineer.cores import EgressCore

class ExternalDataSource():
    '''
    This class simulates an external data source into which data can be loaded.
    '''
    
    def __init__(self, name) -> None:
        self.name = name
    
    def connect(self):
        '''
        Function that simulates a way of connecting to an external data source, where some resources are reserved.        
        ''' 
        print(f"Connected to the Resource: {self.name}.")
    
    def disconnect(self):
        '''
        Function that simulates a way of disconnecting to an external data source, where some resources are released.        
        ''' 
        print(f"Disconnected from the Resource: {self.name}.")
        
    def load(self, data):
        '''
        Function that simulates a way of loading a data to an external data source.        
        ''' 
        print("Loading:", data)
    
    def commit(self):
        '''
        Function that simulates a way of checkpointing/committing loaded data to an external data source.        
        ''' 
        print(f"Saving loaded data to the Resource: {self.name}.")


class LoadData(EgressCore):
    
    def __init__(self, source: ExternalDataSource, input: Iterable | Any = None) -> NoReturn:
        self.source = source
        
        super().__init__(
            input, # The data to be loaded 
            heartbeat = 3, # The frequence at which pulse function is called and backpressure is applied. e.g. 1 means every single record
            forgiving = False, # When true skip a record if it fails to be loaded. Useful when network type exception occur, however may cause resource leak if bad code is writted.
            backpressure = 3 # The amount of delay to be applied at every heartbeat. In seconds.
        )
    
    def constructor(self) -> NoReturn:
        self.source.connect()
    
    def destructor(self, exc_type, exc_value, traceback) -> NoReturn:
        self.source.disconnect()
    
    def pulse(self) -> NoReturn:
        self.source.commit()
        
    def callback(self, record: Any, exception: Exception) -> NoReturn:
        # Either ignore or log the exception
        ...
        
    def consume(self, record: Any) -> NoReturn:
        self.source.load(record)


def main():
    
    data = [
        {"id": 32, "name": "Alice", "age": 25, "city": "New York"},
        {"id": 87, "name": "Bob", "occupation": "Engineer", "salary": 75000},
        {"id": 49, "product": "Laptop", "price": 1200, "brand": "Dell"},
        {"id": 15, "title": "Manager", "department": "HR", "experience": 8},
        {"id": 73, "movie": "Inception", "rating": 9.3, "year": 2010},
        {"id": 21, "name": "Emma", "hobby": "Photography", "favorite_color": "Blue"},
        {"id": 64, "country": "Canada", "population": 38000000, "capital": "Ottawa"},
        {"id": 39, "book": "1984", "author": "George Orwell", "genre": "Dystopian"},
        {"id": 58, "vehicle": "Tesla Model 3", "type": "Electric", "range": 353},
        {"id": 92, "sport": "Soccer", "team": "Barcelona", "coach": "Xavi Hernandez"}
    ]
    
    with LoadData(source=ExternalDataSource("PostgresDB"), input=data) as core:
        core.run()
    
if __name__ == '__main__':
    main()