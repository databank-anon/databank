
from apps import test
from databank.imports import *
__stack__ = None

def hello(uid):
    global __stack__
    if ('msg' not in locals()):
        msg = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    msg = Cell('Hi')
    msg.add_inputs(__stack__.all())
    ___0 = test.sql(Cell('SELECT name FROM users WHERE uid = ?0'), Cell([uid]))
    name = ___0[Cell(0)][Cell(0)]
    name.add_inputs(__stack__.all())
    ___1 = Cell((name != Cell('')))
    if ___1:
        __stack__.push()
        __stack__.add(___1.inputs)
        msg = ((msg + Cell(', ')) + name)
        msg.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(test.id_, Cell(___1, adopt=__stack__.all()).inputs, [], [], auto=True)
        msg.add_inputs(__stack__.all())
        msg.add_inputs(___1.inputs)
    __r__ = Cell(msg, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@test.route('hello/<int:uid>')
def _hello(uid):
    global __stack__
    __stack__ = Stack()
    uid = test.register('hello', 'uid', uid)
    (__r__, __s__, __a__, __u__) = hello(uid)
    logreturn(test.id_, test.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__
