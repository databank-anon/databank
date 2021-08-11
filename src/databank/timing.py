from time import time
import json
from os.path import exists

def timing(fn, key):
    def inner(func):
        def wrapper(*args, **kwargs):
            s = time()
            r = func(*args, **kwargs)
            t = time() - s
            if not exists(fn):
                js = {}
            else:
                try:
                    with open(fn, 'r') as f:
                        js = json.load(f)
                except:
                    js = {}
            if key not in js:
                js[key] = 0
            js[key] += t
            with open(fn, 'w') as f:
                json.dump(js, f)
            return r
        return wrapper
    return inner

def timed_class(Cl, fn, key):
    class TimedClass(type(Cl)):
        @classmethod
        def __prepare__(metacls, name, bases, **kwargs):
            return super().__prepare__(name, bases, **kwargs)
        def __new__(cls, clsname, bases, _dict, **kwargs):
            ndict = {}
            for name, val in _dict.items():
                if val.__class__.__name__ == "function":
                    @timing(fn, key)
                    def wrapper(*args, **kwargs):
                        return val(*args, **kwargs)
                    wrapper.__name__ = val.__name__
                    ndict[name] = wrapper
                else:
                    ndict[name] = val
            return super().__new__(cls, clsname, bases, ndict)
        def __init__(cls, name, bases, namespace, **kwargs):
            super().__init__(name, bases, namespace)
    return TimedClass

