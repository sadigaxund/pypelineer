# UTILS
import itertools

# TYPING
from abc import (
    ABC as AbstractClass,
    ABCMeta as AbstractMetadata,
    abstractmethod as AbstractMethod
)
from typing import (
    Iterable,
    Union,
    Any,
)



class AbstractCore(AbstractClass):
    @property
    def input(self) -> Iterable:
        return self._input
    
    @input.setter
    def input(self, new_input: Union[Iterable, Any]):
        if not isinstance(new_input, Iterable):
            new_input = [new_input]
            
        self._input = itertools.chain(new_input)