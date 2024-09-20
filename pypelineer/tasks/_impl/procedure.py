from ._templates import DoesNothing
from ._functools import clean_raise

from typing import Any

class Procedure:
    ThatDoesNothing: 'Procedure' = None

    def __init__(self, callback) -> None:
        self.callback = callback

    def execute(self, *args, **kwargs) -> Any:
        try:
            return self.callback(*args, **kwargs)
        except Exception as e:
            # TODO: DO BETTER
            raise e
            # clean_raise(e)

    def __call__(self, *args, **kwargs) -> Any:
        return self.execute(*args, **kwargs)
        
        
Procedure.ThatDoesNothing = Procedure(DoesNothing)