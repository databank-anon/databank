from ast import *
from databank import sql
import astunparse

class CFGError(Exception):
    def __init__(self, msg):
        super().__init__(f'CFGError: {msg}')

class InputDependent(CFGError):
    def __init__(self, what):
        super().__init__(f'{what} must be an input-independent string')

RESERVED_NAMES = {"len": 1, "keys": 1, "int": 1, "float": 1, "str": 1, "print": 1, "loginput": -1}
APP_FUNCTIONS = {"me": 0, "name": 0, "now": 0, "now_utc": 0, "get": 1, "post": 1, "method": 0,
                 "get_session": 1, "pop_session": 1, "set_session": 2, "call": (2,float('inf')), "sql": (1,3)}

def is_app_fun(x, app_name):
    return isinstance(x, Attribute) and isinstance(x.value, Name) and x.value.id == app_name \
        and x.attr in APP_FUNCTIONS

def is_sql(x, app_name):
    return is_app_fun(x, app_name) and x.attr == "sql"

def is_call(x, app_name):
    return is_app_fun(x, app_name) and x.attr == "call"

def is_sess(x, app_name):
    return is_app_fun(x, app_name) and x.attr in ["set_session", "pop_session"]

def is_constant(x):
    return isinstance(x, Constant) or isinstance(x, Num) \
        or isinstance(x, Str) or isinstance(x, Bytes) \
        or isinstance(x, NameConstant)

def is_entrypoint(x):
    for decorator in x.decorator_list:
        if isinstance(decorator, Call) and isinstance(decorator.func, Attribute) \
           and decorator.func.attr in ["route", "callback"]:
            return True
    return False

def all_args(x):
    return (x.args.posonlyargs if hasattr(x.args, 'posonlyargs') else []) + x.args.args + x.args.kwonlyargs

class CFG:

    def _memory_location(self, f, j, x):
        slices = []
        last_is_constant = False
        while isinstance(x, Subscript):
            if isinstance(x.slice, Index):
                if is_constant(x.slice.value):
                    slices.append(x.slice)
                    last_is_constant = True
                else:
                    slices = []
                    last_is_constant = False
            else:
                raise CFGError(f'Encountered ill-formed slice ({f}, {j})')
            x = x.value
        if isinstance(x, Name):
            slices.append(x)
        else:
            raise CFGError(f'Encountered ill-formed assignment ({f}, {j})')
        if len(slices) > 1:
            y = z = Subscript()
            for slice_ in slices[:-2]:
                z.value = Subscript()
                z.slice = slice_
                z.ctx = Load()
                z = z.value
            z.value = slices[-1]
            z.slice = slices[-2]
            z.ctx = Store()
        else:
            y = slices[0]    
        return y

    def _default_info(self):
        return {"mem": set(), "ret": False, "cri": False, "vars": set(),
                "tabs": set(), "sess": set(), "call": set()}

    def _check_call(self, x):
        fun_name = x.func.id
        # check whether called function exists
        if fun_name not in self.funs:
            raise CFGError(f'Call to non-existing function {fun_name}')
        args = self.funs[fun_name].args
        # reject starargs and kwargs
        if args.vararg or args.kwarg:
            raise CFGError(f'Encountered *args or **kwargs in call to function {fun_name}')
        # check positional arguments
        if not hasattr(args, 'posonlyargs'):
            args.posonlyargs = []
        n_posonlyargs, n_args = len(args.posonlyargs), len(args.args)
        if len(x.args) < n_posonlyargs:
            raise CFGError(f'Function {fun_name} takes {n_posonlyargs} positional arguments but it is used with {len(x.args)} positional inputs')
        # check that keyword arguments are not duplicated
        if len(set(k.arg for k in x.keywords)) != len(x.keywords):
            raise CFGError(f'Duplicated argument in call to function {fun_name}')
        kwargs_rest = set(k.arg for k in args.args[len(x.args) - n_posonlyargs:])
        # check that all keyword arguments provided are valid
        if set(k.arg for k in x.keywords if k.arg not in kwargs_rest): 
            raise CFGError(f'Invalid keyword arguments in call to function {fun_name}')

    def _called_funs(self, x):
        if isinstance(x, BoolOp):
            if len(x.values) != 2:
                raise CFGError(f'Encountered non-binary BoolOp')
            return self._called_funs(x.values[0]) | self._called_funs(x.values[1])
        elif isinstance(x, BinOp):
            return self._called_funs(x.left) | self._called_funs(x.right)
        elif isinstance(x, UnaryOp):
            return self._called_funs(x.operand)
        elif isinstance(x, Dict):
            return set(fun for key in x.keys for fun in self._called_funs(key)) \
                | set(fun for value in x.values for fun in self._called_funs(value))
        elif isinstance(x, Compare):
            if len(x.comparators) != 1:
                raise CFGError(f'Encountered non-binary Compare')
            return self._called_funs(x.left) | self._called_funs(x.comparators[0])
        elif isinstance(x, Call):
            if isinstance(x.func, Name):
                if x.func.id in RESERVED_NAMES:
                    if len(x.args) != RESERVED_NAMES[x.func.id]:
                        raise CFGError((f'Invalid arguments in call to function {x.func.id} '
                                        f'({RESERVED_NAMES[x.func.id]} arguments expected, got {len(x.args)})'))
                    elif len(x.keywords):
                        raise CFGError(f'Invalid keyword arguments in call to function {x.func.id}')
                    else:
                        return set()
                else:
                    self._check_call(x)
                    funs = {x.func.id}                    
                    for arg in x.args:
                        funs |= self._called_funs(arg)
                    for kw in x.keywords:
                        funs |= self._called_funs(kw.value)
                    return funs
            elif is_app_fun(x.func, self.app_name):
                n = APP_FUNCTIONS[x.func.attr]
                if type(n) is int:
                    if len(x.args) != n:
                        raise CFGError((f'Invalid arguments in call to function {x.func.attr} '
                                        f'({n} arguments excepted, got {len(x.args)})'))
                    return set()
                elif type(n) is tuple and len(n) == 2:
                    if n[0] > len(x.args) or len(x.args) >= n[1]:
                        raise CFGError((f'Invalid arguments in call to function {x.func.attr} '
                                        f'({n[0]}-{n[1]} arguments excepted, got {len(x.args)})'))
                    return set()
                else:
                    raise CFGError(f'Encountered invalid function call to {x.func.attr}')
                if x.func.attr == "call":
                    if not (isinstance(x.func.args[0], Constant) or isinstance(x.func.args[0], Str)):
                        raise InputDependent("address in call")
                    if not (isinstance(x.func.args[1], Constant) or isinstance(x.func.args[1], Str)):
                        raise InputDependent("function in call")
            else:
                raise CFGError(f'Encountered invalid function call')
        elif is_constant(x):
            return set()
        elif isinstance(x, Subscript):
            funs = set()
            if isinstance(x.slice, Index):
                funs |= self._called_funs(x.slice.value)
            else:
                raise CFGError(f'Encountered ill-formed assignment')
            return funs | self._called_funs(x.value)
        elif isinstance(x, Name):
            if x.id == self.app_name:
                raise CFGError(f'App name {self.app_name} cannot be used as variable name')
            elif x.id in self.funs:
                return {x.id}
            else:
                return set()
        elif isinstance(x, Attribute):
            return set()
        elif isinstance(x, List):
            return set(fun for elt in x.elts for fun in self._called_funs(elt))
        elif isinstance(x, Tuple):
            return set(fun for elt in x.elts for fun in self._called_funs(elt))
        else:
            raise CFGError(f'Encountered unknown class {x.__class__.__name__} in _called_funs')

    def _u(self, a, b):
        return {"mem": a["mem"] | b["mem"],
                "ret": a["ret"] | b["ret"],
                "cri": a["cri"] | b["cri"],
                "vars": a["vars"] | b["vars"],
                "tabs": a["tabs"] | b["tabs"],
                "sess": a["sess"] | b["sess"],
                "call": a["call"] | b["call"]}
        
    def _var_tab_sess(self, x):
        if isinstance(x, BoolOp):
            if len(x.values) != 2:
                raise CFGError(f'Encountered non-binary BoolOp')
            return self._u(self._var_tab_sess(x.values[0]), self._var_tab_sess(x.values[1]))
        elif isinstance(x, BinOp):
            return self._u(self._var_tab_sess(x.left), self._var_tab_sess(x.right))
        elif isinstance(x, UnaryOp):
            return self._var_tab_sess(x.operand)
        elif isinstance(x, Dict):
            o = self._default_info()
            for key in x.keys:
                o = self._u(o, self._var_tab_sess(key))
            for value in x.values:
                o = self._u(o, self._var_tab_sess(value))
            return o
        elif isinstance(x, Compare):
            if len(x.comparators) != 1:
                raise CFGError(f'Encountered non-binary Compare')
            return self._u(self._var_tab_sess(x.left), self._var_tab_sess(x.comparators[0]))
        elif isinstance(x, Call):
            o = self._default_info()
            if isinstance(x.func, Name):
                for arg in x.args:
                    o = self._u(o, self._var_tab_sess(arg))
                for kw in x.keywords:
                    o = self._u(o, self._var_tab_sess(kw.value))
                return o
            elif is_sql(x.func, self.app_name):
                if isinstance(x.args[0], Str):
                    ast = sql.parse(x.args[0].s)
                else:
                    ast = sql.parse(x.args[0].value)
                if not isinstance(ast, sql.Select):
                    o["cri"] = True
                if len(x.args) > 0 and (isinstance(x.args[0], Constant) or isinstance(x.args[0], Str)):
                    if len(x.args) > 1:
                        o = self._u(o, self._var_tab_sess(x.args[1]))
                    if not isinstance(ast, sql.Select):
                        o["tabs"].add(ast.table)
                    if isinstance(ast, sql.Insert):
                        if (ast.column_list is None) or ("id" in ast.column_list.columns):
                            raise CFGError(f'ID field in INSERT statement')
                    return o
                else:
                    raise InputDependent(f'Table name in SQL request')
            elif is_sess(x.func, self.app_name):
                if len(x.args) > 0 and (isinstance(x.args[0], Constant) or isinstance(x.args[0], Str)):
                    if len(x.args) > 1:
                        o = self._u(o, self._var_tab_sess(x.args[1]))
                    if isinstance(x.args[0], Str):
                        o["sess"].add(x.args[0].s)
                    else:
                        o["sess"].add(x.args[0].value)
                    return o
                else:
                    raise InputDependent(f'Session variable name in SQL request')
            elif is_call(x.func, self.app_name):
                o["cri"] = True
                if len(x.args) > 0 and (isinstance(x.args[0], Constant) or isinstance(x.args[0], Str)):
                    if len(x.args) > 2:
                        o = self._u(o, self._var_tab_sess(x.args[2]))
                    if isinstance(x.args[0], Str):
                        o["call"].add(x.args[0].s)
                    else:
                        o["call"].add(x.args[0].value)
                    return o
                else:
                    raise InputDependent(f'Address in call')
            else:
                return self._default_info()
        elif is_constant(x):
            return self._default_info()
        elif isinstance(x, Subscript):
            o = self._default_info()
            if isinstance(x.slice, Index):
                o = self._u(o, self._var_tab_sess(x.slice.value))
            else:
                raise CFGError(f'Encountered ill-formed subscript')
            return self._u(o, self._var_tab_sess(x.value))
        elif isinstance(x, Name):
            o = self._default_info()
            if x.id not in self.funs and x.id not in RESERVED_NAMES:
                o["vars"].add(x.id)
            return o
        elif isinstance(x, Attribute):
            return self._default_info()
        elif isinstance(x, List) or isinstance(x, Tuple):
            o = self._default_info()
            for elt in x.elts:
                o = self._u(o, self._var_tab_sess(elt))
            return o
        else:
            raise CFGError(f'Encountered unknown class {x.__class__.__name__} in _var_tab_sess')
        
    def _cfg_expr(self, x, node):
        cfs = self._called_funs(x)
        if node not in self.E:
            self.E[node] = set()
        for cf in cfs:
            self.E[node].add(('forward', (cf, (0,))))

    def _cfg_stmt(self, x, fun_name, j):
        node = (fun_name,tuple(j))
        if isinstance(x, Assign):
            if len(x.targets) != 1:
                raise CFGError(f'Encountered multiple-target assignment ({f}, {j})')
            self.V[node] = self._u(self._var_tab_sess(x.value), self._var_tab_sess(x.targets[0]))
            self.V[node]["mem"] = self._memory_location(fun_name, tuple(j), x.targets[0])
            if node not in self.E:
                self.E[node] = set()
            for target in x.targets:
                self._cfg_expr(target, node)
            return (node, [node], [])
        elif isinstance(x, AugAssign):
            self.V[node] = self._u(self._var_tab_sess(x.value), self._var_tab_sess(x.target))
            self.V[node]["mem"] = self._memory_location(fun_name, tuple(j), x.target)
            if node not in self.E:
                self.E[node] = set()
            self._cfg_expr(x.target, node)
            return (node, [node], [])
        elif isinstance(x, Delete):
            if len(x.targets) != 1:
                raise CFGError(f'Encountered multiple-target delete ({f}, {j})')
            self.V[node] = self._var_tab_sess(x.targets[0])
            self.V[node]["mem"] = self._memory_location(fun_name, tuple(j), x.targets[0])
            if node not in self.E:
                self.E[node] = set()
            for target in x.targets:
                self._cfg_expr(target, node)
            return (node, [node], [])
        elif isinstance(x, Return):
            if hasattr(x, 'value'):
                self.V[node] = self._var_tab_sess(x.value)
                self._cfg_expr(x.value, node)
            else:
                self.V[node] = self._default_info()
            self.V[node]["ret"] = True
            if node not in self.E:
                self.E[node] = set()
            return (node, [], [node])
        elif isinstance(x, While):
            (first, last, ret) = self._cfg_block(x.body, fun_name, j)
            self.V[node] = self._var_tab_sess(x.test)
            if node not in self.E:
                self.E[node] = set()
            self.E[node].add(('forward', first))
            self._cfg_expr(x.test, node)
            for last_el in last:
                self.E[last_el].add(('forward', node))
            if x.orelse != []:
                raise CFGError(f'Encountered else block in while loop ({f}, {j})')
            assert(x.orelse == [])
            return (node, [node] + last, ret)
        elif isinstance(x, If):
            (first, last, ret) = self._cfg_block(x.body, fun_name, ['body'] + j)
            self.V[node] = self._var_tab_sess(x.test)
            if node not in self.E:
                self.E[node] = set()
            self.E[node].add(('forward', first))
            last2 = []
            if x.orelse:
                (first2, last2, ret2) = self._cfg_block(x.orelse, fun_name, ['orelse'] + j)
                self.E[node].add(('forward', first2))
                return (node, last + last2, ret + ret2)
            return (node, [node] + last, ret)
        elif isinstance(x, Pass) or isinstance(x, Global):
            self.V[node] = self._default_info()
            if node not in self.E:
                self.E[node] = set()
            return (node, [node], [])
        elif isinstance(x, Expr):
            self._cfg_expr(x.value, node)
            self.V[node] = self._var_tab_sess(x.value)
            if node not in self.E:
                self.E[node] = set()
            return (node, [node], [])
        else:
            raise CFGError(f'Encountered unknown class {x.__class__.__name__} in stmt')

    def _cfg_block(self, b, fun_name, j):
        first, last, ret = None, [], []
        for jj, x in enumerate(b):
            (first2, last2, ret2) = self._cfg_stmt(x, fun_name, [jj] + j)
            if last:
                for last_el in last:
                    if not self.V[last_el]["ret"]:
                        self.E[last_el].add(('forward', first2))
            else:
                first = first2
            last = last2
            ret += ret2
        return (first, last, ret)

    def _cfg_fun(self, fun_name):
        if fun_name in self.F:
            return self.F[fun_name]
        self.F[fun_name] = self._cfg_block(self.funs[fun_name].body + [Return()], fun_name, [])
        return self.F[fun_name]

    def _add_back_edges(self):
        to_add = set()
        for (v, ws) in self.E.items():
            for w in ws:
                if w[0][0] == 'forward' and w[0][1] != v[0]:
                    for x in self.F[w[0][1]][2]:
                        to_add.add((x, v))
        for a in to_add:
            self.E[a[0]].add(('back', a[1]))

    def __init__(self, x, app_name):
        if isinstance(x, Module):
            self.funs = {}
            self.V, self.E, self.F = {}, {}, {}
            self.app_name = app_name
            for fun in x.body:
                if isinstance(fun, FunctionDef):
                    self.funs[fun.name] = fun
                    if fun.name[:3] == "db_":
                        raise CFGError(f'Illegal prefix db_ in function name {fun.name}')
                    if fun.name[0] == "_":
                        raise CFGError(f'Illegal prefix _ in function name {fun.name}')
                    if fun.name in self.F:
                        raise CFGError(f'Two functions named {fun.name} in mod')
                    if fun.name == self.app_name:
                        raise CFGError(f'App name {{self.app_name}} cannot be used as function name')
                    if (hasattr(fun.args, 'vararg') and fun.args.vararg) or \
                       (hasattr(fun.args, 'kwarg') and fun.args.kwarg):
                        raise CFGError(f'Encountered *args or **kwargs in function definition')
                    for arg in all_args(fun):
                        if arg.arg == self.app_name:
                            raise CFGError(f'App name {self.app_name} cannot be used as argument name')
                else:
                    # simply ignore this, will be caught in dbast
                    pass
            for fun_name in self.funs:
                self._cfg_fun(fun_name)
            self._add_back_edges()
        else:
            raise CFGError(f'Encountered unknown class {x.__class__.__name__} in mod')

    def _assigned(self, node, within=None, seen=None, same_fun=True, forward_only=False):
        seen = seen or set()
        if (node, same_fun) in seen or (node, True) in seen:
            return set()
        seen.add((node, same_fun))
        mems = {}
        for neigh in self.E[node]:
            if (neigh[0] == 'forward' or not forward_only) and \
               (within is None or (not same_fun) or (neigh[1][0], neigh[1][1][-len(within[1]):]) == within):
                mems.update(self._assigned(neigh[1], within=within, seen=seen,
                                           same_fun=(same_fun and neigh[1][0] == node[0]),
                                           forward_only=forward_only))
        if same_fun and self.V[node]["mem"]:
            mem = self.V[node]["mem"]
            mems[astunparse.unparse(mem)] = ('local', mem)
        for t in self.V[node]["tabs"]:
            mems[('table', t)] = ('table', t)
        for t in self.V[node]["sess"]:
            mems[('session', t)] = ('session', t)
        return mems

    def assigned(self, node, within=None, forward_only=False):
        return set(self._assigned(node, within=within, forward_only=forward_only).values())

    def _called(self, node, within=None, seen=None, same_fun=True, forward_only=False):
        seen = seen or set()
        if (node, same_fun) in seen or (node, True) in seen:
            return set()
        seen.add((node, same_fun))
        calls = set()
        for neigh in self.E[node]:
            if (neigh[0] == 'forward' or not forward_only) and \
               (within is None or (not same_fun) or (neigh[1][0], neigh[1][1][-len(within[1]):]) == within):
                calls |= self._called(neigh[1], within=within, seen=seen,
                                      same_fun=(same_fun and neigh[1][0] == node[0]),
                                      forward_only=forward_only)
        if same_fun and self.V[node]["call"]:
            calls |= self.V[node]["call"]
        return calls

    def called(self, node, within=None, forward_only=False):
        return self._called(node, within=within, forward_only=forward_only)

    def locals(self, node, fun=None, seen=None):
        seen = seen or set()
        fun = fun or node[0]
        if node in seen:
            return set()
        seen.add(node)
        mems = set()
        for neigh in self.E[node]:
            if neigh[1][0] == fun:
                mems |= self.locals(neigh[1], fun=fun, seen=seen)
        mems |= self.V[node]["vars"]
        return mems

    def _returns(self, node, within, seen=None):
        seen = seen or set()
        if node in seen:
            return False
        seen.add(node)
        flag = False
        for neigh in self.E[node]:
            if (neigh[1][0], neigh[1][1][-len(within)+1:]) == within:
                flag = flag or self._returns(neigh[1], within, seen=seen)
        flag = flag or self.V[node]["ret"] or self.V[node]["cri"]
        return flag

    def returns(self, node):
        return self._returns(node, node)

