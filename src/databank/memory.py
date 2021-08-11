import json
from copy import deepcopy
import operator
from flask import session

class Cell:
    
    def __init__(self, value, inputs=None, adopt=None):
        if type(value) is list:
            self.value = [Cell(e) for e in value]
        elif type(value) is dict:
            self.value = {k: Cell(v) for (k, v) in value.items()}
        elif type(value) is tuple:
            self.value = tuple(Cell(e) for e in value)
        elif not isinstance(value, Cell):
            self.value = value
        if isinstance(value, Cell):
            self.value = value.value
            self.inputs = {k: v for (k, v) in value.inputs.items()}
        else:
            if type(inputs) is str:
                self.load_inputs(inputs)
            elif type(inputs) is list:
                self.inputs = {}
                for inputs_ in inputs:
                    self.add_inputs(inputs_)
            else:
                self.inputs = deepcopy(inputs) or {}
        if adopt:
            self.add_inputs(adopt)

    #def hash(self):
    #return hashlib.sha256(repr(self.value).encode('utf-8')).hexdigest()

    def all_inputs(self):
        inputs = {i for i in self.inputs}
        if type(self.value) in [list, tuple]:
            for e in self.value:
                inputs |= e.all_inputs()
        elif type(self.value) is dict:
            for e in self.value.values():
                inputs |= e.all_inputs()
        return inputs
    
    def add_inputs(self, inputs_):
        for input_, owner in inputs_.items():
            self.inputs[input_] = owner

    def dump(self):
        if type(self.value) is list:
            return {"type": "list",
                    "value": [e._dump() for e in self.value],
                    "inputs": self.inputs}
        elif type(self.value) is dict:
            return {"type": "dict",
                    "value": {k: v._dump() for (k, v) in self.value.items()},
                    "inputs": self.inputs}
        elif type(self.value) is tuple:
            return {"type": "tuple",
                    "value": tuple(e._dump() for e in self.value),
                    "inputs": self.inputs}
        else:
            return {"type": "value",
                    "value": self.value,
                    "inputs": self.inputs}

    def sanitize(self):
        if type(self.value) is list:
            return [e.sanitize() for e in self.value]
        elif type(self.value) is dict:
            return {k.sanitize(): v.sanitize() for (k, v) in self.value.items()}
        elif type(self.value) is tuple:
            return tuple(e.sanitize() for e in self.value)
        else:
            return self.value

    def sanitize_value(self):
        sanitized = self.sanitize()
        if type(sanitized) in [list, dict, tuple]:
            return None
        else:
            return sanitized or ""

    def __repr__(self):
        return ("<databank.memory.Cell value={} inputs={}>").format(self.value, self.inputs)

    def __bool__(self):
        return bool(self.sanitize())

    def __getitem__(self, key):
        if type(self.value) in [list, tuple]:
            if (isinstance(key, Cell) and type(key.value) is int \
                and key.value >= 0 and key.value < len(self.value)) \
               or (type(key) is int and key >= 0 and key < len(self.value)):
                if isinstance(key, Cell):
                    cell = Cell(self.value[key.value], adopt=key.inputs)
                else:
                    cell = Cell(self.value[key])
                cell.add_inputs(self.inputs)
                return cell
        elif type(self.value) is dict:
            if (isinstance(key, Cell) and key.value in self.value) or key in self.value:
                if isinstance(key, Cell):
                    cell = Cell(self.value[key.value], adopt=key.inputs)
                else:
                    cell = Cell(self.value[key])
                cell.add_inputs(self.inputs)
                return cell
        if isinstance(key, Cell):
            return Cell(None, inputs=key.inputs, adopt=self.inputs)
        else:
            return Cell(None, inputs=self.inputs)

    def __setitem__(self, key, value):
        if type(self.value) in [list, dict] and \
           (isinstance(key, Cell) and type(key.value) not in [list, dict, tuple] or \
            type(key) not in [list, dict, tuple]):
            if isinstance(key, Cell):
                self.value[key.value] = value
            else:
                self.value[key] = value

    def __delitem__(self, key):
        if type(self.value) in [list, dict] and \
           (isinstance(key, Cell) and type(key.value) not in [list, dict, tuple] or \
            type(key) not in [list, dict, tuple]):
            if isinstance(key, Cell):
                del self.value[key.value]
            else:
                del self.value[key]
            
## Additional functions

def _len(cell):
    if type(cell.value) in [list, tuple, dict]:
        return Cell(len(cell.value), inputs=cell.inputs)
    else:
        return Cell(None, inputs=cell.inputs)
    
def _keys(cell):
    if type(cell.value) is dict:
        return Cell(list(cell.value.keys()), inputs=cell.inputs)
    else:
        return Cell(None, inputs=cell.inputs)

def _int(cell):
    try:
        assert(type(cell.value) not in [list, tuple, dict])
        return Cell(int(cell.value), inputs=cell.inputs)
    except:
        return Cell(None, inputs=cell.inputs)

def _float(cell):
    try:
        assert(type(cell.value) not in [list, tuple, dict])
        return Cell(float(cell.value), inputs=cell.inputs)
    except:
        return Cell(None, inputs=cell.inputs)
    
def _str(cell):
    try:
        assert(type(cell.value) not in [list, tuple, dict])
        return Cell(str(cell.value), inputs=cell.inputs)
    except:
        return Cell(None, inputs=cell.inputs)

def _print(cell):
    print(repr(cell))

def non(cell):
    return Cell(not cell.value, inputs=cell.inputs)

## Add overloaded operators to Cell

BINOPS = ["__add__", "__sub__", "__mul__", "__div__", "__mod__", "__divmod__", "__pow__", "__lshift__",
          "__rshift__", "__and__", "__xor__", "__or__", "__radd__", "__rsub__", "__rmul__", "__rdiv__",
          "__rmod__", "__rdivmod__", "__rpow__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__",
          "__ror__", "__lt__", "__le__", "__eq__", "__ne__", "__gt__", "__ge__", "__contains__"]

for o in BINOPS:
    def wrapper(self, other, o=o):
        if isinstance(other, Cell):
            try:
                return Cell(operator.__dict__[o](self.value, other.value), inputs=self.inputs, adopt=other.inputs)
            except:
                return Cell(None, inputs=self.inputs, adopt=other.inputs)
        else:
            try:
                return Cell(operator.__dict__[o](self.value, other), inputs=self.inputs)
            except:
                return Cell(None, inputs=self.inputs, adopt=other.inputs)
    setattr(Cell, o, wrapper)

UNOPS = ["__neg__", "__pos__", "__invert__"]
        
for o in UNOPS:
    def wrapper(self, o=o):
        try:
            return Cell(operator.__dict__[o](self.value), inputs=self.inputs)
        except:
            return Cell(None, inputs=self.inputs)
    setattr(Cell, o, wrapper)

class Stack:

    def __init__(self):
        self.stack = [{}]

    def pop(self):
        self.stack.pop()

    def push(self):
        self.stack.append({})

    def add(self, inputs, bot=False):
        for input_, owner in inputs.items():
            self.stack[0 if bot else -1][input_] = owner

    def all(self):
        inputs = {}
        for inputs_ in self.stack:
            for input_, owner in inputs_.items():
                inputs[input_] = owner
        return inputs
                
def load(value):
    if value["type"] == "list":
        return Cell([load(e) for e in value["value"]], inputs=value["inputs"])
    elif value["type"] == "dict":
        return Cell({k: load(v) for (k, v) in value["value"].items()}, inputs=value["inputs"])
    elif value["type"] == "tuple":
        return Cell(tuple(load(e) for e in value["value"]), inputs=value["inputs"])
    else:
        return Cell(value["value"], inputs=value["inputs"])
