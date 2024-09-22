# UTILS
from .abtract import AbstractCore
from ._functools import MultiFunction, CoreNamespace

# TYPING
from abc import (
    ABCMeta as AbstractMetadata,
)

# TODO: Make sure after all the processor functions are cleared and renamed into 'process', user should see only that one instead of original names

class ProcessMetaCore(AbstractMetadata):
    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)
    
    def __new__(cls, name, bases, dct):
        
        # Skip below manipulations on parent class
        if AbstractCore in bases:
            return super().__new__(cls, name, bases, dct)
        
        # Merge all processor methods into single object
        accumulative = None
        for key in dct.copy():
            attr = dct[key]
            
            # Get those methods that are marked as processor
            if accumulative == None and isinstance(attr, MultiFunction):
                accumulative = attr
                # Remove accumulated properties from namespace
                del dct[key]
                
        # Add newly formed accumulative processor as attribute
        dct['process'] = accumulative
        return super().__new__(cls, name, bases, dct)

def processor(func):
    if not hasattr(processor, 'namespaces'):
        processor.namespaces = {}
    
    module_name = func.__qualname__.split('.')[0]
    if not module_name in processor.namespaces:
        processor.namespaces[module_name] = CoreNamespace()
    return processor.namespaces[module_name].register(func)

class ProcessCore(AbstractCore, metaclass=ProcessMetaCore):
    ...
    
    