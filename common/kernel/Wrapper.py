import inspect


class Wrapper:
    def __init__(self, wrapped=None):
        self.wrap(wrapped)

    def wrap(self, wrapped):
        self.wrapped = wrapped
        if wrapped is not None:
            self.__class__ = wrapped.__class__
            self.__dict__.update(wrapped.__dict__)
            for n, m in inspect.getmembers(wrapped, callable):
                """Return whether the object is callable (i.e., some kind of function).
                Note that classes are callable, as are instances of classes with a
                __call__() method."""  
        
                if not n.startswith('_'):
                    setattr(self, n, m)
