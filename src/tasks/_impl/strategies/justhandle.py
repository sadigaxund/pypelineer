from .._templates import void_exception_handler
from .base import BaseStrategy
from typing import Any, Callable, NoReturn

class JustHandleStrategy(BaseStrategy):
    def __init__(self, 
                 fallback_value: Any = None, 
                 on_error: Callable[[Exception], Any] = void_exception_handler, 
                 ) -> NoReturn:
        super().__init__(fallback_value=fallback_value, 
                         on_error=on_error, 
                         blacklist=False, 
                         whitelist=True)