from .Types import *

class SourceNode:
    def __init__(self, udf_extractor) -> None:
        self.output = udf_extractor
    
    def __input__(self):
        raise AttributeError("SourceNode does not take input")

    def __input__(self):
        raise NotImplementedError("Output was not linked!")

    @property
    def output(self) -> DefaultOutputType:
        return self.__output__()

    @output.setter
    def output(self, value: DefaultInputType):
        def new_output_function():
            yield from value

        self.__output__ = new_output_function
