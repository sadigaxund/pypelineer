from typing import Any, Tuple
from .....cores.implement.junction import *


class DuplicateRecordCore(Core):
    
    # TODO: Implement Deepcopy
    def __init__(self, times = 2) -> None:
        self.times = times
        super().__init__()
    
    def segregate(self, record: Any) -> Tuple[Any]:
        return tuple([record] * self.times)
