from ast import *
import astunparse
from databank.cfg import CFG, RESERVED_NAMES, APP_FUNCTIONS, is_app_fun, all_args, is_sql, is_call
from databank import sql

class ConversionError(Exception):
    def __init__(self, msg):
        super().__init__(f'ConversionError: {msg}')
        
i = 0
def new_var():
    global i
    i += 1
    return "___{}".format(i-1)

def process_expr(x, app_name, node, cfg):
    if isinstance(x, BoolOp):
        if len(x.values) != 2:
            raise ConversionError(f'Encountered non-binary BoolOp')
        code0, x0 = process_expr(x.values[0], app_name, node, cfg)
        code1, x1 = process_expr(x.values[1], app_name, node, cfg)
        y = Call(func=Name(id="Cell", ctx=Load()),
                 args=[BoolOp(op=x.op, values=[Attribute(value=x0, attr="value", ctx=Load()),
                                               Attribute(value=x1, attr="value", ctx=Load())])],
                 keywords=[keyword(arg="inputs",
                                   value=Call(func=Name(id="dict", ctx=Load()),
                                              args=[Attribute(value=x0, attr="inputs", ctx=Load())],
                                              keywords=[],
                                              kwargs=Attribute(value=x1, attr="inputs", ctx=Load())))])
        return code0 + code1, y
    elif isinstance(x, BinOp):
        code_l, x_l = process_expr(x.left, app_name, node, cfg)
        code_r, x_r = process_expr(x.right, app_name, node, cfg)
        return code_l + code_r, BinOp(left=x_l, op=x.op, right=x_r)
    elif isinstance(x, UnaryOp):
        code_o, x_o = process_expr(x.operand, app_name, node, cfg)
        if isinstance(x.op, Not):
            return code_o, Call(func=Name(id="non", ctx=Load()), args=[x_o], keywords=[])
        else:
            return code_o, UnaryOp(op=x.op, operand=x_o)
    elif isinstance(x, Compare):
        if len(x.comparators) != 1:
            raise ConversionError(f'Encountered non-binary Compare')
        code_l, x_l = process_expr(x.left, app_name, node, cfg)
        code_r, x_r = process_expr(x.comparators[0], app_name, node, cfg)
        return code_l + code_r, Call(func=Name(id="Cell", ctx=Load()),
                                     args=[Compare(x_l, x.ops, [x_r])], keywords=[])
    elif isinstance(x, Call):
        is_app_fun_call = is_app_fun(x.func, app_name)
        if not isinstance(x.func, Name) and not is_app_fun_call:
            raise ConversionError(f'Encountered ill-formed function call')
        if isinstance(x.func, Name) and x.func.id in RESERVED_NAMES:
            y = Name(id="db_" + x.func.id, ctx=Load())
        else:
            y = x.func
        code, args, kws = [], [], []
        #if (x.func.id not in RESERVED_NAMES) and not is_app_fun_call:
        #code.append(Expr(value=Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
        #attr="push", ctx=Load()),
        #args=[], keywords=[])))
        for arg in x.args:
            code_a, x_a = process_expr(arg, app_name, node, cfg)
            code += code_a
            args.append(x_a)
        for kw in x.keywords:
            code_k, x_k = process_expr(kw, app_name, node, cfg)
            code += code_k
            kws.append(x_k)
        v = new_var()
        if is_sql(x.func, app_name):
            # try:
            #     v = sql(...)
            # except Stop as __stop__:
            #     {% for a in assigned(s) %}
            #     a.add_inputs(__stop__.inputs)
            #     {% endfor %}
            #     raise __stop__
            # else:
            #     __stack__.add(v.inputs, bot=True)
            parsed_sql = sql.parse(x.args[0].s if isinstance(x.args[0], Str) else x.args[0].value)
            if isinstance(parsed_sql, sql.Insert) or isinstance(parsed_sql, sql.Delete):
                kws.append(keyword(arg='stack', value=Name(id="__stack__", ctx=Load())))
                kws.append(keyword(arg='assigned', value=List(
                    elts=[Constant(value=tab) for (typ, tab) in cfg.assigned(node) if typ == 'table'],
                    ctx=Load())))
                kws.append(keyword(arg='called', value=List(
                    elts=[Constant(value=callee) for callee in cfg.called(node)] + \
                         [Call(func=Attribute(value=Name(id=app_name, ctx=Load()), attr="me", ctx=Load()),
                               args=[], keywords=[])],
                          ctx=Load())))
                except_code = []
                for m in cfg.assigned(node):
                    _if_while_adopt("__stop__", m, except_code, app_name, stack=False)
                except_code.append(Raise(exc=Name(id="__stop__", ctx=Load()),
                                         cause=None))
                code.append(Try(body=[Assign(targets=[Name(id=v, ctx=Store())],
                                             value=Call(func=y, args=args, keywords=kws))],
                                handlers=[ExceptHandler(type=Name(id="Stop", ctx=Load()),
                                                        name="__stop__",
                                                        body=except_code)],
                                orelse=[Expr(value=Call(
                                    func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                   attr="add", ctx=Load()),
                                    args=[Attribute(value=Name(id=v, ctx=Load()),
                                                    attr="inputs", ctx=Load())],
                                    keywords=[keyword(arg="bot", value=Constant(value=True))]))],
                                finalbody=None))
            else:
                code.append(Assign(targets=[Name(id=v, ctx=Store())],
                                   value=Call(func=y, args=args, keywords=kws)))
        elif is_call(x.func, app_name):
            # try:
            #     v = call(...)
            # except Stop as __stop__:
            #     {% for a in assigned(s) %}
            #     a.add_inputs(__stop__.inputs)
            #     {% endfor %}
            #     raise __stop__
            # else:
            #     __stack__.add(v.inputs, bot=True)
            kws.append(keyword(arg='stack', value=Name(id="__stack__", ctx=Load())))
            kws.append(keyword(arg='assigned', value=List(
                    elts=[Constant(value=tab) for (typ, tab) in cfg.assigned(node) if typ == 'table'],
                    ctx=Load())))
            kws.append(keyword(arg='called', value=List(
                    elts=[Call(func=Name(id="Cell", ctx=Load()), args=[Constant(value=callee)], keywords=[])
                          for callee in cfg.called(node)] + \
                         [Call(func=Attribute(value=Name(id=app_name, ctx=Load()), attr="me", ctx=Load()),
                               args=[], keywords=[])],
                          ctx=Load())))
            except_code = []
            for m in cfg.assigned(node):
                _if_while_adopt("__stop__", m, except_code, app_name, stack=False)
            except_code.append(Raise(exc=Name(id="__stop__", ctx=Load()),
                                     cause=None))
            code.append(Try(body=[Assign(targets=[Tuple(elts=[Name(id=v, ctx=Store()),
                                                              Name(id="__i__", ctx=Store())],
                                                        ctx=Store())],
                                         value=Call(func=y, args=args, keywords=kws))],
                            handlers=[ExceptHandler(type=Name(id="Stop", ctx=Load()),
                                                    name="__stop__",
                                                    body=except_code)],
                            orelse=[Expr(value=Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                                   attr="add", ctx=Load()),
                                                    args=[Name(id="__i__", ctx=Load())],
                                                    keywords=[keyword(arg="bot", value=Constant(value=True))]))],
                            finalbody=None))
        elif isinstance(x.func, Name) and x.func.id not in RESERVED_NAMES:
            # try:
            #     v = f(...)
            # except Stop as __stop__:
            #     {% for a in assigned(s) %}
            #     a.add_inputs(__stop__.all())
            #     {% endfor %}
            #     raise __stop__
            except_code = []
            for m in cfg.assigned(node):
                _if_while_adopt("__stop__", m, except_code, app_name, stack=False)
            except_code.append(Raise(exc=Name(id="__stop__", ctx=Load()),
                                     cause=None))
            code.append(Try(body=[Assign(targets=[Name(id=v, ctx=Store())],
                                         value=Subscript(value=Call(func=y, args=args, keywords=kws),
                                                         slice=Constant(value=0), ctx=Load()))],
                            handlers=[ExceptHandler(type=Name(id="Stop", ctx=Load()),
                                                    name="__stop__",
                                                    body=except_code)],
                            orelse=None, finalbody=None))
        elif isinstance(x.func, Attribute) and x.func.attr in ["get", "post"]:
            code.append(Assign(targets=[Name(id=v, ctx=Store())],
                               value=Call(func=y, args=[Constant(value=node[0])] + args, keywords=kws)))
        else:
            code.append(Assign(targets=[Name(id=v, ctx=Store())],
                               value=Call(func=y, args=args, keywords=kws)))
        return code, Name(id=v, ctx=Load())
    elif isinstance(x, Constant) or isinstance(x, NameConstant):
        return [], Call(func=Name(id="Cell", ctx=Load()), args=[Constant(value=x.value)], keywords=[])
    elif isinstance(x, Num):
        return [], Call(func=Name(id="Cell", ctx=Load()), args=[Constant(value=x.n)], keywords=[])
    elif isinstance(x, Str):
        return [], Call(func=Name(id="Cell", ctx=Load()), args=[Constant(value=x.s)], keywords=[])
    elif isinstance(x, Subscript):
        code_v, x_v = process_expr(x.value, app_name, node, cfg)
        if isinstance(x.slice, Index):
            code_i, x_i = process_expr(x.slice.value, app_name, node, cfg)
            code_s, slice_ = code_i, Index(x_i)
        else:
            raise ConversionError("Encountered unknown class {} in subscript".format(x.__class__))
        return code_v + code_s, Subscript(value=x_v, slice=slice_, ctx=x.ctx)
    elif isinstance(x, Name):
        if x.id[:2] == '__':
            raise ConversionError(f'Cannot use double underscore variables')
        return [], x
    elif isinstance(x, Attribute):
        return [], x
    elif isinstance(x, List):
        ## Cell([Cell(x_1), ..., Cell(x_n)])
        code_l, x_es = [], []
        for elt in x.elts:
            code_e, x_e = process_expr(elt, app_name, node, cfg)
            code_l += code_e
            x_es.append(x_e)
        x_l = Call(func=Name(id="Cell", ctx=Load()), args=[List(elts=x_es, ctx=Load())], keywords=[])
        return code_l, x_l
    elif isinstance(x, Dict):
        ## Cell({ k[1].value: Cell(v_1), ..., k[n].value: Cell(v_n) }, inputs=[k[1].inputs, ..., k[n].inputs])
        code_d, x_ks, x_vs = [], [], []
        n = len(x.keys)
        for key in x.keys:
            code_k, x_k = process_expr(key, app_name, node, cfg)
            code_d += code_k
            x_ks.append(x_k)
        code_d.append(Assign(targets=[Name(id="__k__", ctx=Store())],
                             value=List(elts=x_ks, ctx=Load())))
        for value in x.values:
            code_v, x_v = process_expr(value, app_name, node, cfg)
            code_d += code_v
            x_vs.append(x_v)
        x_d = Call(func=Name(id="Cell", ctx=Load()),
                   args=[Dict(keys=[Attribute(value=Subscript(value=Name(id="__k__", ctx=Load()),
                                                              slice=Constant(value=i)),
                                              attr="value") for i in range(n)],
                              values=x_vs)],
                   keywords=[keyword(arg="inputs",
                                     value=List(elts=[Attribute(value=Subscript(value=Name(id="__k__", ctx=Load()),
                                                                                slice=Constant(value=i)),
                                                                attr="inputs") for i in range(n)],
                                                ctx=Load()))])
        return code_d, x_d
    elif isinstance(x, Tuple):
        ## Cell((Cell(x_1), ..., Cell(x_n)))
        code_t, x_es = [], []
        for elt in x.elts:
            code_e, x_e = process_expr(elt, app_name, node, cfg)
            code_t += code_e
            x_es.append(x_e)
        x_t = Call(func=Name(id="Cell", ctx=Load()), args=[Tuple(elts=x_es, ctx=Load())], keywords=[])
        return code_t, x_t
    else:
        raise ConversionError("Encountered unknown class {} in expr".format(x.__class__))

def assign_slices(x, app_name, node, cfg):
    if isinstance(x, Subscript):
        if not isinstance(x.slice, Index):
            raise ConversionError(f'Encountered ill-formed subscript')
        code_s, s = process_expr(x.slice.value, app_name, node, cfg)
        code_v, v = assign_slices(x.value, app_name, node, cfg)
        return code_s + code_v, v + [s]
    elif isinstance(x, Name) or isinstance(x, Attribute):
        code, y = process_expr(x, app_name, node, cfg)
        return code, [y]
    else:
        #todo
        pass

def _if_while_prefix(v, cfg, node):
    if_code = []
    if_code.append(Expr(value=Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                  attr="push", ctx=Load()),
                                   args=[], keywords=[])))
    if_code.append(Expr(value=Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                  attr="add", ctx=Load()),
                                   args=[Attribute(Name(id=v, ctx=Load()),
                                                   attr="inputs", ctx=Load())],
                                   keywords=[])))
    return if_code

def _if_while_sanitize(v, cfg, node, app_name):
    return [Expr(value=Call(func=Name(id="logsanitize", ctx=Load()),
                            args=[Attribute(value=Name(id=app_name, ctx=Load()), attr="id_", ctx=Load()),
                                  Attribute(value=Call(func=Name(id="Cell", ctx=Load()),
                                                       args=[Name(id=v, ctx=Load())],
                                                       keywords=[keyword(arg="adopt", value=Call(func=Attribute(
                                                           value=Name(id="__stack__", ctx=Load()),
                                                           attr="all", ctx=Load()), args=[], keywords=[]))]),
                                            attr="inputs",  ctx=Load()),
                                  List(elts=[Constant(value=m) for (k, m) in cfg.assigned(node, within=node)
                                             if k == "table"]),
                                  List(elts=[Constant(value=u) for u in cfg.called(node, within=node)])],
                            keywords=[keyword(arg="auto", value=Constant(value=True))] + \
                            ([keyword(arg="u", value=Call(func=Attribute(
                                value=Name(id=app_name, ctx=Load()), attr="me", ctx=Load()),
                                                          args=[], keywords=[]))]
                             if cfg.returns(node) else [])))]

def _if_while_adopt(v, m, else_code, app_name, stack=True):
    if m[0] == "local":
        if stack:
            else_code.append(Expr(value=Call(func=Attribute(value=m[1], attr="add_inputs", ctx=Load()),
                                             args=[Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                                       attr="all", ctx=Load()),
                                                        args=[], keywords=[])],
                                             keywords=[])))
        else_code.append(Expr(value=Call(func=Attribute(value=m[1], attr="add_inputs", ctx=Load()),
                                         args=[Attribute(value=Name(id=v, ctx=Load()),
                                                         attr="inputs", ctx=Load())],
                                         keywords=[])))
    elif m[0] == "table":
        if stack:
            else_code.append(Expr(value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                            attr="add_sql_inputs", ctx=Load()),
                                             args=[Constant(value=m[1]),
                                                   Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                                       attr="all", ctx=Load()),
                                                        args=[], keywords=[])],
                                             keywords=[])))
        else_code.append(Expr(value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                        attr="add_sql_inputs", ctx=Load()),
                                         args=[Constant(value=m[1]),
                                               Attribute(value=Name(id=v, ctx=Load()),
                                                         attr="inputs", ctx=Load())],
                                         keywords=[])))
    elif m[0] == "session":
        if stack:
            else_code.append(Expr(value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                            attr="add_session_inputs", ctx=Load()),
                                             args=[Constant(value=m[1]),
                                                   Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                                       attr="all", ctx=Load()),
                                                        args=[], keywords=[])],
                                             keywords=[])))
        else_code.append(Expr(value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                        attr="add_session_inputs", ctx=Load()),
                                         args=[Constant(value=m[1]),
                                               Attribute(value=Name(id=v, ctx=Load()),
                                                         attr="inputs", ctx=Load())],
                                         keywords=[])))
    else:
        assert(False)

def _process_if_while_body(i, b, cfg, v, app_name, new_i, within):
    node = (i[-1], tuple(i[:-1]))
    if_code = _if_while_prefix(v, cfg, node)
    if_code += [s for t in map(lambda y: process_stmt([y[0]] + new_i + i, y[1], cfg, app_name), enumerate(b)) for s in t]
    if_code.append(Expr(value=Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                  attr="pop", ctx=Load()),
                                   args=[], keywords=[])))
    else_code = []
    if cfg.returns(node):
        else_code.append(Expr(value=Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                        attr="add", ctx=Load()),
                                         args=[Attribute(value=Name(id=v, ctx=Load()),
                                                         attr="inputs", ctx=Load())],
                                         keywords=[keyword(arg="bot", value=Constant(value=True))]))) 
    for m in cfg.assigned(node, within=within):
        _if_while_adopt(v, m, else_code, app_name)
    return if_code, else_code

def process_if_body(i, b, cfg, v, app_name, branch='body'):
    return _process_if_while_body(i, b, cfg, v, app_name, [branch], (i[-1], tuple([branch] + i[:-1])))

def process_while_body(i, b, cfg, v, app_name):
    return _process_if_while_body(i, b, cfg, v, app_name, [], (i[-1], tuple(i[:-1])))
                    
def process_assign(b, n, slices, code):
    code.append(Assign(targets=[Name("__slv__", Store())],
                       value=List(elts=slices[1:], ctx=Load())))
    code.append(Assign(targets=[Name("__w__", Store())], value=slices[0]))
    for_code = []
    for_code.append(Expr(value=Call(func=Attribute(value=Name(id="__w__", ctx=Load()), attr="add_inputs"),
                                    args=[Attribute(value=Subscript(value=Name(id="__slv__", ctx=Load()),
                                                                    slice=Name(id="__i__", ctx=Load()),
                                                                    ctx=Load()),
                                                    attr="inputs", ctx=Load())],
                                    keywords=[])))
    for_code.append(If(test=Compare(left=Name(id="__i__", ctx=Load()),
                                    ops=[Eq()],
                                    comparators=[Constant(value=n-1)]),
                       body=b,
                       orelse=[If(test=Compare(left=Subscript(value=Name(id="__slv__", ctx=Load()),
                                                              slice=Name(id="__i__", ctx=Load()),
                                                              ctx=Store()),
                                               ops=[In()],
                                               comparators=[Name(id="__w__", ctx=Load())]),
                                  body=[Assign(targets=[Name(id="__w__", ctx=Store())],
                                               value=Subscript(value=Name(id="__w__", ctx=Load()),
                                                               slice=Subscript(value=Name(id="__slv__", ctx=Load()),
                                                                               slice=Name(id="__i__", ctx=Load()),
                                                                               ctx=Load()),
                                                               ctx=Load()))],
                                  orelse=[Break()])]))
    code.append(For(target=Name(id="__i__", ctx=Store()),
                    iter=Call(func=Name(id="range", ctx=Load()),
                              args=[Constant(value=n)],
                              keywords=[]),
                    body=for_code,
                    orelse=[]))

def set_local(x):
    return If(test=Compare(left=Constant(value=x), ops=[NotIn()],
                           comparators=[Call(func=Name(id="locals", ctx=Load()), args=[], keywords=[])]),
              body=[Assign(targets=[Name(id=x, ctx=Store())],
                           value=Call(func=Name("Cell", ctx=Load()), args=[Constant(value=None)], keywords=[]))],
              orelse=[])

def process_stmt(i, x, cfg, app_name):
    if len(i) > 1:
        node = (i[-1], tuple(i[:-1]))
    if isinstance(x, FunctionDef):
        if i != []:
            raise ConversionError(f'Encountered internal function ({i})')
        code = []
        my_args = [Name(id=arg.arg, ctx=Load()) for arg in all_args(x)]
        my_args_ids = [arg.id for arg in my_args]
        y = FunctionDef()
        y.name = x.name
        y.args = x.args
        y.body = [Global(["__stack__"])] \
                 + [set_local(x) for x in cfg.locals((x.name, (0,))) if x not in my_args_ids] \
                 + [s for t in map(lambda y: process_stmt([y[0], x.name] + i, y[1], cfg, app_name), enumerate(x.body)) for s in t]
        if not isinstance(y.body[-1], Return):
            y.body.append(Assign(targets=[Name(id="__s__", ctx=Store())],
                                 value=Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                           attr="all", ctx=Load()),
                                            args=[], keywords=[])))
            y.body.append(Return(value=Tuple(elts=[Constant(value=None),
                                                   Name(id="__s__", ctx=Load()),
                                                   List(elts=[], ctx=Load()),
                                                   List(elts=[], ctx=Load())])))
        for decorator in x.decorator_list:
            if not isinstance(decorator, Call) or not isinstance(decorator.func, Attribute) \
               or not isinstance(decorator.func.value, Name) or (decorator.func.value.id != app_name) \
               or decorator.func.attr not in ["route", "callback"]:
                raise ConversionError(f'Encountered ill-formed decorator ({i})')
        y.decorator_list = []
        y.returns = x.returns
        code.append(y)
        # additional _f function for entrypoints
        # @decorators
        # def _f(x_1, ..., x_n):
        #     global __stack__
        #     __stack__ = Stack()
        #     x_1 = {{app_name}}.register('f', 'x_1', x_1)
        #     ...
        #     x_n = {{app_name}}.register('f', 'x_n', x_n)
        #     __r__, __s__, __a__, __u__ = f(x_1, ..., x_n)
        #     logreturn({{app_name}}.id_, {{app_name}}.me(), __r__, __s__, __a__, __u__, auto=True)
        #     return __r__
        if x.decorator_list:
            _y = FunctionDef()
            _y.name = "_" + y.name
            _y.args = y.args
            _y.body = [Global(["__stack__"]),
                       Assign(targets=[Name(id="__stack__", ctx=Store())],
                              value=Call(func=Name(id="Stack", ctx=Load()), args=[], keywords=[]))] \
                      + [Assign(targets=[Name(id=arg.id, ctx=Store())],
                                value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                          attr="register", ctx=Load()),
                                           args=[Constant(value=y.name),
                                                 Constant(value=arg.id),
                                                 Name(id=arg.id, ctx=Load())], keywords=[]))
                         for arg in my_args] \
                      + [Assign(targets=[Tuple(elts=[Name(id="__r__", ctx=Store()), Name(id="__s__", ctx=Store()),
                                                     Name(id="__a__", ctx=Store()), Name(id="__u__", ctx=Store())])],
                                value=Call(func=Name(id=y.name, ctx=Load()), args=my_args, keywords=[])),
                         Expr(value=Call(func=Name(id="logreturn", ctx=Load()),
                                         args=[Attribute(value=Name(id=app_name, ctx=Load()),
                                                         attr="id_", ctx=Load()),
                                               Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                                   attr="me", ctx=Load()), args=[], keywords=[]),
                                               Name(id="__r__", ctx=Store()), Name(id="__s__", ctx=Store()),
                                               Name(id="__a__", ctx=Store()), Name(id="__u__", ctx=Store())],
                                         keywords=[keyword(arg="auto", value=Constant(value=True))])),
                         Return(value=Name(id="__r__", ctx=Load()))]
            _y.decorator_list = x.decorator_list
            _y.returns = x.returns
            code.append(_y)
        return code
    elif isinstance(x, Return):
        ## return y ->
        ##
        ## {% for session a in assigned(s) %}
        ## a.add_inputs(__stack__.all())
        ## {% endfor %}
        ## __r__ = Cell(y, adopt=__stack__.all())
        ## __s__ = stack.all()
        ## {% for each level of if and while loops entered %}
        ## __stack__.pop()
        ## {% end %}
        ## return __r__, __s__, { table in assigned(s) }, called(s)
        code, y = process_expr(x.value, app_name, node, cfg)
        assigned = []
        # remove this
        for m in cfg.assigned(node, within=(i[-1], ()), forward_only=True):
            if m[0] == "table":
                assigned.append(m[1])
            elif m[0] == "session":
                code.append(Expr(value=Call(func=Attribute(value=Name(id=app_name, ctx=Load()),
                                                           attr="add_session_inputs", ctx=Load()),
                                            args=[Constant(value=m[1]),
                                                  Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                                      attr="all", ctx=Load()),
                                                       args=[], keywords=[])],
                                            keywords=[])))
        # remove this -- end
        code.append(Assign(targets=[Name(id="__r__", ctx=Store())],
                           value=Call(func=Name(id="Cell", ctx=Load()),
                                      args=[y],
                                      keywords=[keyword(arg="adopt", value=Call(
                                          func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                         attr="all", ctx=Load()),
                                          args=[], keywords=[]))])))
        code.append(Assign(targets=[Name(id="__s__", ctx=Store())],
                           value=Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                     attr="all", ctx=Load()),
                                      args=[], keywords=[])))
        for _ in range(len([j for j in i if type(j) is int])-1):
            code.append(Expr(value=Call(func=Attribute(value=Name("__stack__", ctx=Load()),
                                                       attr="pop", ctx=Load()),
                                        args=[], keywords=[])))
        code.append(Return(value=Tuple(elts=[Name(id="__r__", ctx=Load()), Name(id="__s__", ctx=Load()),
                                             List(elts=[Constant(value=a) for a in assigned], ctx=Load()),
                                             List(elts=[Constant(value=u) for u in
                                                        cfg.called(node, within=(i[-1], ()), forward_only=True)],
                                                  ctx=Load())])))
        return code
    elif isinstance(x, Delete):
        ## del[e1]...[en] ->
        ##
        ## __w__ = id
        ## __slv__ = [e1, ..., en]
        ## for __i__ in range({{n}}):
        ##     __w__.adopt(__slv__[__i__].inputs)
        ##     if __i__ == {{n}}-1:
        ##         del __w__[__slv__[__i__]]
        ##     elif __slv__[__i__] in __w__:
        ##          __w__ = __w__[__slv__[__i__]]
        ##     else:
        ##          break
        ## id.adopt(__stack__.all())
        if len(x.targets) != 1:
            raise ConversionError(f'Encountered multiple-target delete ({i})')
        code = []
        code_s, slices = assign_slices(x.targets[0], app_name, i, cfg)
        code += code_s
        if not isinstance(slices[0], Name):
            raise ConversionError(f'Encountered ill-formed delete ({i})')
        n = len(slices) - 1
        deletion = Delete(targets=[Subscript(value=Name(id="__w__", ctx=Store()),
                                             slice=Subscript(value=Name(id="__slv__", ctx=Load()),
                                                             slice=Name(id="__i__", ctx=Load()),
                                                             ctx=Store()),
                                             ctx=Store())])
        process_assign([deletion], n, slices, code)
        code.append(Expr(value=Call(func=Attribute(value=slices[0], attr="add_inputs", ctx=Load()),
                                    args=[Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                              attr="all", ctx=Load()),
                                               args=[], keywords=[])],
                                    keywords=[])))
        return code
    elif isinstance(x, Assign):
        if len(x.targets) != 1:
            raise ConversionError(f'Encountered multiple-target assignment ({i})')
        code = []
        code_s, slices = assign_slices(x.targets[0], app_name, i, cfg)
        code += code_s
        if not isinstance(slices[0], Name):
            raise ConversionError(f'Encountered ill-formed assignment ({i})')
        code_v, x_v = process_expr(x.value, app_name, node, cfg)
        code += code_v
        n = len(slices) - 1
        ## id[e1]...[en] = e' ->
        ##
        ## __w__ = id
        ## __slv__ = [e1, ..., en]
        ## for __i__ in range({{n}}):
        ##     __w__.adopt(__slv__[__i__].inputs)
        ##     if __i__ == {{n}}-1:
        ##          __w__[__slv__[__i__]] = e'
        ##     elif __slv__[__i__] in __w__:
        ##          __w__ = __w__[__slv__[__i__]]
        ##     else:
        ##          break
        ## id.adopt(__stack__.all())
        if n:
            assignment = Assign(targets=[Subscript(value=Name(id="__w__", ctx=Store()),
                                                   slice=Subscript(value=Name(id="__slv__", ctx=Load()),
                                                                   slice=Name(id="__i__", ctx=Load()),
                                                                   ctx=Store()),
                                                   ctx=Store())],
                                value=x_v)
            process_assign([assignment], n, slices, code)
        else:
            code.append(Assign(targets=[slices[0]], value=x_v))
        code.append(Expr(value=Call(func=Attribute(value=slices[0], attr="add_inputs", ctx=Load()),
                                    args=[Call(func=Attribute(value=Name(id="__stack__", ctx=Load()),
                                                              attr="all", ctx=Load()),
                                               args=[], keywords=[])],
                                    keywords=[])))
        return code
    elif isinstance(x, AugAssign):
        return process_stmt(i, Assign(targets=[x.target], value=BinOp(left=x.target, op=x.op, right=x.value)),
                            cfg, app_name)
    elif isinstance(x, If):
        ## If(e1, b1, b2) ->
        ##
        ## newvar = e1
        ## if newvar:
        ##     __stack__.push()
        ##     __stack__.add(newvar.inputs)
        ##     b1
        ##     __stack__.pop()
        ## else:
        ##     logsanitize({{app_name}}.id_, Call(newvar, adopt=__stack__.all()).inputs, assigned(b1), called(b1){% if returns(b1) %}, u = meetup.me(){% endif %})
        ##     {% if returns(b1) %}
        ##     __stack__.add(newvar.inputs, bot=True)
        ##     {% endif %}
        ##     {% for m in assigned(b1) %}
        ##     m.add_inputs(__stack__.all())
        ##     m.add_inputs(newvar.inputs)
        ##     {% endfor %}
        ## if not newvar:p
        ##    [idem for b2]
        code = []
        code_t, t = process_expr(x.test, app_name, node, cfg)
        code += code_t
        v = new_var()
        code.append(Assign(targets=[Name(id=v, ctx=Store())], value=t))
        if_code, else_code = process_if_body(i, x.body, cfg, v, app_name)
        else_code = _if_while_sanitize(v, cfg, node, app_name) + else_code
        code.append(If(test=Name(id=v, ctx=Load()), body=if_code, orelse=else_code))
        if x.orelse:
            if_code_else, else_code_else = process_if_body(i, x.orelse, cfg, v, app_name, 'orelse')
            else_code_else = _if_while_sanitize(v, cfg, node, app_name) + else_code_else
            code.append(If(test=Call(func=Name(id="non", ctx=Load()),
                                     args=[Name(id=v, ctx=Load())], keywords=[]),
                           body=if_code_else, orelse=else_code_else))
        return code
    elif isinstance(x, While):
        ## While(e1, b1) ->
        ##
        ## newvar = e1
        ## while newvar:
        ##     __stack__.push()
        ##     __stack__.add(newvar.inputs)
        ##     b1
        ##     __stack__.pop()
        ##     newvar = e1
        ## logsanitize({{app_name}}.id_, Call(newvar, adopt=__stack__.all()).inputs, assigned(b1), called(b1))
        ## {% if returns(b1) %}
        ## __stack__.add(newvar.inputs)
        ## {% endif %}
        ## {% for m in assigned(b1) %}
        ## m.add_inputs(__stack__.all())
        ## m.add_inputs(newvar.inputs)
        ## {% endfor %}
        if x.orelse != []:
            raise ConversionError(f'Encountered else block in while loop ({i})')
        code = []
        code_t, t = process_expr(x.test, app_name, node, cfg)
        code += code_t
        v = new_var()
        assign_t = Assign(targets=[Name(id=v, ctx=Store())], value=t)
        code.append(assign_t)
        while_code, else_code = process_while_body(i, x.body, cfg, v, app_name)
        else_code = _if_while_sanitize(v, cfg, node, app_name) + else_code
        code.append(While(test=Name(id=v, ctx=Load()),
                          body=while_code + code_t + [assign_t],
                          orelse=[]))
        code += else_code
        return code
    elif isinstance(x, Import) or isinstance(x, ImportFrom) or isinstance(x, Global):
        raise ConversionError(f'Encountered illegal import')
    elif isinstance(x, Pass):
        return [x]
    elif isinstance(x, Expr):
        code_e, e = process_expr(x.value, app_name, node, cfg)
        return code_e
    else:
        raise ConversionError("Encountered unknown class {} in stmt".format(x.__class__))
        return [x]
    
def check_imports(x, app_name):
    return len(x.body) >= 1 \
        and (astunparse.unparse(x.body[0]) == astunparse.unparse(
            ImportFrom(module="apps", names=[alias(name=app_name, asname=None)], level=0)))
    
def process_mod(x, cfg, app_name):
    if isinstance(x, Module):
        y = Module()
        if not check_imports(x, app_name):
            raise ConversionError("Ill-formed module (should import application first)")
        y.body = x.body[:1] + \
                 [ImportFrom(module="databank.imports", names=[alias(name="*", asname=None)], level=0)] + \
                 [Assign(targets=[Name(id="__stack__", ctx=Store())], value=Constant(value=None))] + \
                 [s for t in map(lambda x: process_stmt([], x, cfg, app_name), x.body[1:]) for s in t]
        return y
    else:
        raise ConversionError("Encountered unknown class {} in mod".format(x.__class__))

def convert_code(code, app_name):
    parsed_code = parse(code)
    cfg = CFG(parsed_code, app_name)
    return astunparse.unparse(process_mod(parsed_code, cfg, app_name)), cfg


# bad output? bad sql etc.

# check existence of routes, tables etc.
# add try catch around sql operations
