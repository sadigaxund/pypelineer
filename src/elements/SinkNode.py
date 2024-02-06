
from .Types import *
from abc import ABC, ABCMeta


class SinkNode:
    
    # LOADER 
    def __loader__(self, value: Any) -> Any:
        raise NotImplementedError("The load function was not implemented!")

    @property
    def loader(self) -> Callable[[DefaultOutputType], Optional[bool]]:
        # TODO: Ensure self
        return self.__loader__

    @loader.setter
    def loader(self, new_loader: Callable) -> None:
        self.__loader__ = new_loader

    # OUTPUT
    def __output__(self):
        raise NoOutputAttributeWarning(self)
    
    # INPUT
    def __input__(self):
        raise InputNotLinkedError

    @property
    def input(self) -> DefaultOutputType:
        return self.__input__()

    @input.setter
    def input(self, value: DefaultInputType):
        if not isinstance(value, DefaultInputType):
            raise ValueError(
                f"Input has to be either of type Generator, Iterator or Collection. Recieved: {type(value)}"
            )

        def create_input_function():
            yield from value

        self.__input__ = create_input_function
        
    # MAIN LOGIC
    # Options:
    #     1. Pass individual loader function(as udf) and apply over all records
    #     2. Pass mass loader function that has implementation to load all records
    #     3. Use Custom loader function: KafkaLoader
    
    def load_one(self): ...
    def load_bulk(self): ...
    # You can run manually:

    # or Let the node do its jon
        
    
    def __init__(self) -> None:
        self.future_value = None
        pass
    
    
    SENTINEL = 0x73656E74696E656C
    
    def __next__(self):
        if self.future_value is not None:
            self.future_value = None
            return self.future_value
        try:
            return next(self.input)
        except StopIteration:
            return SinkNode.SENTINEL
    
    def more(self):
        # cases:
        # 1. if f_val not None or sentinel -> then use it
        # 2. if f_val is None -> we don't know, go fetch
        # 3. if f_val is SENTINEL -> gameover
        match self.future_value:
            case None:
                # means we could still have something
                self.future_value = self.__next__()
                if self.future_value == SinkNode.SENTINEL:
                    return False
                ...
            case SinkNode.SENTINEL:
                # means it already ended
                return False
                ...
            case _:
                # means we already checked before, and there is at least f_val
                return True
            
    def load_record(self, record):
        raise NotImplemented("Functionality to load record was not implemented!")
    
    def load_bulk(self):        
        try:
            # Started Loading...
            while True:
                value = yield  # get value from as you go
                self.load_record(value)
        finally:
            # Finished Loading...
            ...
    
    def start(self):
        self.ETL = self.load_bulk()
        self.ETL.send(None) # Generator (for loader) started
    
    def close(self):
        self.ETL.close()  # Generator (for loader) stopped
    
    def __enter__(self): 
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback): 
        self.close()
        
    def step(self) -> bool:
        record = self.__next__()
        
        if record == SinkNode.SENTINEL:
            return True # pipeline done
        
        self.ETL.send(record)
        return False
    
    def run(self, 
            at_start: Callable = None, 
            at_exit: Callable = None, 
            per_iteration: Callable = None, 
            fallback: Callable = None,
            blacklist: List = None,
            whitelist: List = None,
            backoff_seconds: int = 0,
            chunk_size: int = 500) -> None:
        self.start()
        while self.more():
            self.step()
        self.close()
        
    
        
    
        
        

