from typing import Callable

def clean_raise(exception: BaseException):
    exception.__traceback__ = None
    raise exception from None

def fn2key(fn):
    return tuple([
            fn.__module__,
            fn.__class__,
            fn.__name__,
        ])

class MultiFunction(object):
    def __init__(self, fn = None):
        self.functions = list()
        
        if isinstance(fn, MultiFunction):
            self.extend(fn)
        elif isinstance(fn, Callable):
            self.functions.append(fn)
        
    def __call__(self, *args, **kwargs):
        result = None
        
        for fn in self.functions:
            result = fn(*args, **kwargs)
            args = (result,)

        return result
    
    
    def __add__(self, new_fn):
        if not isinstance(new_fn, Callable):
            raise TypeError("Can't append anything other than object of type Callable.")
        
        if isinstance(new_fn, MultiFunction):
            self.functions.extend(new_fn.functions)
        else:
            self.functions.append(new_fn)
        
        return self
 
    def __str__(self) -> str:
        return str(self.functions)
        
    def key(self):
        fn = self.functions[0] if len(self.functions) > 0 else None
        
        if fn:
            return fn2key(fn)
        else:
            return tuple()


class CoreNamespace:
    def __init__(self) -> None:
        self.functions = MultiFunction()

    def register(self, fn):
        self.functions += fn
        return self.functions
