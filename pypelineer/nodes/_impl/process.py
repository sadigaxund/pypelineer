from ...cores import ProcessCore
from .abtract import AbstractNode

# TYPING
from typing import NoReturn, Iterable

class ProcessNode(AbstractNode):
    def __init__(self, *processor_cores: ProcessCore, input: Iterable = None) -> NoReturn:
        super().__init__(processor_cores, input = input)
    
    def __iter__(self):
        return self.output
        
    @property
    def output(self):
        # SIMPLER: return map(self.core.process, self.input)
        transformed_output = self.input
        for acore in self.core:
            transformed_output = map(acore.process, transformed_output)
        
        return transformed_output
