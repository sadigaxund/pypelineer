from typing import NoReturn
from ...cores.junction import DuplicateRecordCore
from .....nodes._impl.junction import JunctionNode


class DuplicateRecordNode(JunctionNode):
    def __init__(self, times=2, input=None) -> NoReturn:
        super().__init__(DuplicateRecordCore(times), times, input)
