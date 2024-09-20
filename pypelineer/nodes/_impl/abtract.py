# TOOLS
from ...cores import AbstractCore

# TYPING
from abc import (
    ABC as AbstractClass,
    ABCMeta as AbstractMetadata,
)
from typing import (
    Iterable,
    Any,
    NoReturn,
    Union
)
# Iterable | Any

class Shiftable:
    def __rshift__(self: 'AbstractNode', other: 'AbstractNode'):
        other.input = self.output
        return other
    
    def __lshift__(self: 'AbstractNode', other: 'AbstractNode'):
        self.input = other.output
        return self

class AbstractNode(AbstractClass, Shiftable, metaclass=AbstractMetadata):
    def __init__(self, core: AbstractCore, input = None) -> NoReturn:
        self.core = core
        # init placeholder variables
        self.__input=input
        self.__output=None
        
    @property
    def input(self) -> Iterable:
        return self.__input
    
    @input.setter
    def input(self, value: Union[Iterable, Any]):
        self.__input = value

    @property
    def output(self) -> Iterable:
        return self.__output

    def __iter__(self):
        return self.output
        
    
    # @output.setter
    # def output(self, value):
    #     self.__output = value
        
   