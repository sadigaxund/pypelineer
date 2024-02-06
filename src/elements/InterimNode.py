from .Types import *

class InterimNode:

    def __init__(self, udf_executor, input=None) -> None:
        self.executor = udf_executor
        
        if input:
            self.input = input
        
    # EXECUTOR
    def __executor__(self, value: Any) -> Any:
        return value  # no change

    @property
    def executor(self) -> Callable:
        # TODO: Ensure self
        return self.__executor__

    @executor.setter
    def executor(self, new_executor: Callable) -> None:
        self.__executor__ = new_executor

    # OUTPUT
    def __output__(self) -> DefaultOutputType:
        for record in self.__input__():
            # TODO: Surround with try catch,
            # and maybe recieve callback as parameter to deal with bad record
            yield self.executor(record)

    @property
    def output(self) -> DefaultOutputType:
        return self.__output__()

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
