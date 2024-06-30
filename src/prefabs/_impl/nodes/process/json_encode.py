from typing import Iterable, NoReturn
from ...cores.process import AnyJSONEncodeCore
from .....nodes._impl.process import ProcessNode

class AnyJSONEncodeNode(ProcessNode):
    def __init__(self, input: Iterable = None) -> NoReturn:
        super().__init__(AnyJSONEncodeCore, input=input)
    