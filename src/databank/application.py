from flask import Flask, request, session, render_template
import sqlite3
import datetime
import socket
import pickle
import time
from threading import Thread, get_ident, RLock
from copy import deepcopy
from Crypto.Cipher import AES

from databank.monitor import loginsert, logdelete, logreturn, loginput, logsanitize, lock, commit, Stop
from databank.memory import Cell, load
from databank.calls import Server, do_call, join_route, pad
from databank.timing import timing
import databank.sql as sql
from settings import get_db, FUNDAMENTAL, is_set

class Cur:
    def __init__(self, db, lock, select_only=False):
        self.db = db
        self.lock = lock
        self.select_only = select_only
    def __enter__(self):
        if not self.select_only:
            self.lock.acquire()
        self.cur = self.db.cursor()
        return self.cur
    def __exit__(self, type, value, traceback):
        self.cur.close()
        if not self.select_only:
            self.db.commit()
            self.lock.release()
            
## Application wrapper
            
class Application:

    def __init__(self, flask, server, id_, app_name, sp_IP, database, key, databank_side=True):
        self.flask = flask
        self.id_ = id_
        self.app_name = app_name
        if databank_side:
            self.server = server
        else:
            self.server = Server(databank_side=False)            
        self.server.register_app(id_, sp_IP, key)
        self.database = database
        self.aes = AES.new(bytes(key, 'utf8'), AES.MODE_EAX)
        self.databank_side = databank_side
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.cursor().execute("PRAGMA synchronous = OFF")
        self.lock = RLock()
        self.sql_asts = {}

    def __del__(self):
        self.db.close()

    # Function decorators

    def callback(self, rule):
        def inner(f):
            def wrapper(*args, **kw):
                x = f(*args, **kw)
                return x.sanitize()
            wrapper.__name__ = str(self.id_) + "__" + f.__name__
            self.server.register_callback(self.id_, rule, self, wrapper)
            return wrapper
        return inner
    
    def route(self, rule, **kwargs):
        def inner(f):
            def wrapper(*args, **kw):
                try:
                    ret = f(*args, **kw)
                except Stop as stop:
                    return render_template("violation.html", **locals())
                if isinstance(ret, Cell):
                    if type(ret.value) in [list, dict, tuple]:
                        return ""
                    else:
                        return ret.sanitize_value()
                else:
                    return ret
            wrapper.__name__ = str(self.id_) + "__" + f.__name__
            return self.flask.route(join_route(self.id_, rule), **kwargs)(wrapper)
        return inner

    # Distant call

    def call(self, addr, function, args, stack=None, assigned=None, called=None, **kwargs):
        args, kwargs = Cell(args), Cell(kwargs)
        args_cell = Cell(None, inputs=(args.all_inputs() | kwargs.all_inputs()))
        if self.databank_side:
            logreturn(self.id_, addr, args_cell, stack.all(), assigned, called, auto=True)
        dump = pickle.dumps((function.value, args.sanitize(), kwargs.sanitize()))
        msg = self.aes.encrypt(pad(dump))
        ret = do_call(msg, addr.value, databank_side=self.databank_side) 
        data = pickle.loads(self.aes.decrypt(ret).strip())
        if self.databank_side:
            cell = Cell(data)
            for arg in args.value:
                cell.add_inputs(arg.inputs)
            for kwarg in kwargs.value.values():
                cell.add_inputs(kwarg.inputs)
            return (cell, {})
        else:
            return data

    # Exposed user input methods

    def method(self):
        return Cell(request.method)

    def post(self, func_name, key):
        if isinstance(key, Cell) and key.inputs:
            raise InputDependent("POST key")
        value = request.form.get(key.value, None)
        return self.register(func_name, key.value, value)

    def get(self, func_name, key):
        if isinstance(key, Cell) and key.inputs:
            raise InputDependent("GET key")
        value = request.args.get(key.value, None)
        return self.register(func_name, key.value, value)

    # Session

    def get_session(self, key):
        if key.value in session and key.value[:4] != "user":
            cell = session[key.value]
            cell.add_inputs(key.inputs)
            return cell
        else:
            return Cell(None, inputs=key.inputs)

    def pop_session(self, key):
        if key.value in session and key.value[:4] != "user":
            session.pop(key.value, None)
        return Cell(None)

    def set_session(self, key, value):
        session[key.value] = value.dump()
        return Cell(None)

    def add_session_inputs(self, key, inputs):
        if key in session:
            cell = load(session[key])
            cell.add_inputs(inputs)
            session[key] = cell.dump()
        else:
            session[key] = Cell(None, inputs=inputs)
        return Cell(None)

    # extension: COOKIES

    def _me(self):
        try:
            return session['user_id']
        except RuntimeError:
            # no active HTTP request → callback
            return self.callback_user_id
    
    def me(self):
        value = self._me()
        return Cell(value)#, inputs={value: value})

    def name(self):
        try:
            value = session['user_name']
            return Cell(value)#, inputs={value: self._me()})
        except RuntimeError:
            # no active HTTP request → callback
            return Cell(self.callback_user_name)#, inputs={value: self._me()})

    # extension: access name and other personal information

    def now(self):
        return int(time.time())

    def now_utc(self):
        return datetime.datetime.utcfromtimestamp(self.now()).strftime('%Y-%m-%d @ %H:%M')
            
    # Database operations

    def db_cur(self, select_only=False):
        return Cur(self.db, self.lock, select_only=select_only)

    def _print_db(self, s):
        if is_set('verbose_db'):
            print(s)

    @timing('../evaluation/time.json', 'database')
    def sql(self, query, args=None, stack=None, assigned=None, called=None):
        if query.value in self.sql_asts:
            ast, where_vars, tables = deepcopy(self.sql_asts[query.value])
        else:
            ast = sql.parse(query.value)
            ast.table = f"{self.id_}_{ast.table}"
            if isinstance(ast, sql.Select):
                # read variables in WHERE clause
                where_vars = set()
                for join in ast.joins:
                    join.table = f"{self.id_}_{join.table}"
                    where_vars |= join.get_vars()
                if ast.where is not None:
                    where_vars |= ast.where.get_vars()
                if ast.order_by is not None:
                    where_vars |= ast.order_by.get_vars()
                # list used tables
                tables = {ast.table} | {join.table for join in ast.joins}
            else:
                where_vars, tables = set(), set()
            self.sql_asts[query.value] = deepcopy(ast), where_vars, tables
        if args is not None:
            ast.set_params(args)
        args_cell = Cell(None)
        args_cell.add_inputs(query.inputs)
        if args is not None:
            args_cell.add_inputs(args.inputs)
            for arg in args.value:
                args_cell.add_inputs(arg.inputs)
        if isinstance(ast, sql.Select):
            # retrieve results
            with self.db_cur(select_only=True) as cur:
                self._print_db(">> " + str(ast))
                cur = cur.execute(str(ast))
                results = cur.fetchall()
                self._print_db("<< " + repr(results))
                # retrieve ids
                ast_ids = deepcopy(ast)
                ast_ids.result_columns = sql.ResultColumns(
                    columns=[sql.Col(table=table, name="id") for table in tables])
                self._print_db(">> " + str(ast_ids))
                cur = cur.execute(str(ast_ids))
                indices = cur.fetchall()
                self._print_db("<< " + repr(indices))
                idx = {}
                inputs = {}
                # for each used table
                for t, table in enumerate(tables):
                    inputs[table] = []
                    ids = [i[t] for i in indices if i[t] is not None]
                    # fill in index
                    idx[table] = {}
                    for j, id_ in enumerate(ids):
                        if id_ not in idx[table]:
                            idx[table][id_] = []
                        idx[table][id_].append(j)
                    # identify relevant vars
                    rel_vars = list(filter(lambda x: "." not in x or x.split('.')[0] == f'"{table}"',
                                                where_vars))
                    rel_vars = [var.split('.')[1] if '.' in var else var for var in rel_vars]
                    # retrieve field-level inputs
                    inputs_q = ("SELECT i.entry, i.field, i.input, i.owner FROM \"{}_inputs_\" AS i "
                                "WHERE i.entry IS NULL OR i.entry IN ({}) OR i.field IN ({})") \
                                .format(table,
                                   ", ".join(map(str, list(set(ids)))),
                                   ", ".join(map(lambda x: "'{}'".format(x), rel_vars)))
                    #print(inputs_q)
                    self._print_db(">> " + inputs_q)
                    cur = cur.execute(inputs_q)
                    for i in cur.fetchall():
                        inputs[table].append((i[0],
                                              i[1] if i[1] in where_vars or (not i[1]) else table + "." + i[1],
                                              i[2], i[3]))
                    self._print_db("<< " + repr(inputs))
                if ast.result_columns.type_ in ["star", "starred"]:
                    star_table = ast.table if ast.result_columns.type_ == "star" \
                        else str(ast.result_columns).split('.')[0].replace('"', '')
                    # read list of columns
                    col_q = "PRAGMA table_info(\"{}\")".format(star_table)
                    self._print_db(">> " + col_q)
                    cur = cur.execute(col_q)
                    columns = [n[1] for n in cur.fetchall()]
                    self._print_db("<< " + repr(columns))
                    col_idx = {star_table + '.' + col: i for (i, col) in enumerate(columns)}
                elif ast.result_columns.type_ == "countstar":
                    col_idx = {}
                else:
                    col_idx = {str(col): i for (i, col) in enumerate(ast.result_columns.columns)}
            # build answer
            cell = Cell([Cell(result) for result in results], inputs=args_cell.inputs)
            # add inputs
            for table in tables:
                for i, field, input_, owner in inputs[table]:
                    # add table-level inputs and inputs from columns in WHERE clause
                    if i is None or field in where_vars:
                        cell.inputs[input_] = owner
                    # add row-level inputs
                    elif field is None and i in idx and idx[i] in cell.value:
                        for j in idx[table][i]:
                            cell.value[j].inputs[input_] = owner
                    # add field-level inputs
                    elif i in idx[table] and field in col_idx:
                        for j in idx[table][i]:
                            cell.value[j].value[col_idx[field]].inputs[input_] = owner
            return cell
        elif isinstance(ast, sql.Insert):
            # insert entries
            # requires a trigger
            with self.db_cur() as cur:
                self._print_db(">> " + str(ast))
                cur.execute(str(ast))
                # read new entries' ids
                new_q = "SELECT * FROM \"{}_new_\"".format(ast.table)
                self._print_db(">> " + new_q)
                cur = cur.execute(new_q)
                entry_ids = [n[0] for n in cur.fetchall()]
                self._print_db("<< " + repr(entry_ids))
                # read list of columns
                col_q = "PRAGMA table_info(\"{}\")".format(ast.table)
                self._print_db(">> " + col_q)
                cur = cur.execute(col_q)
                columns = [n[1] for n in cur.fetchall()]
                self._print_db("<< " + repr(columns))
                # retrieve new entries
                new2_q = "SELECT * FROM \"{}\" WHERE id IN ({})".format(ast.table, ", ".join(map(str, entry_ids)))
                self._print_db(">> " + new2_q)
                cur = cur.execute(new2_q)
                entries = cur.fetchall()
                self._print_db("<< " + str(entries))
                # put inserted entries into memory cell
                ins_cells = {entry[0]: Cell({k: v for (k, v) in zip(columns[1:], entry[1:])},
                                            inputs=args.inputs)
                             for entry in entries}
                # set inputs
                if ast.column_list:
                    column_list = ast.column_list.columns
                else:
                    column_list = columns
                for entry in entries:
                    for (value, column) in zip(ast.values.values, column_list):
                        ins_cells[entry[0]].value[column].add_inputs(value.get_inputs())
                log_cell = Cell(None, inputs=args.inputs)
                try:
                    lock()
                    # for each new entry
                    for (i, ins_cell) in ins_cells.items():
                        # try to log insertion of the entry
                        log_cell.add_inputs(loginsert(self.id_, ast.table, i, ins_cell, stack.all(), assigned, called).inputs)
                # execution was stopped (violation detected)
                except Stop as stop:
                    # reset trace
                    # reset()
                    # remove entries
                    del_q = "DELETE FROM \"{}\" WHERE id IN ({})".format(
                        ast.table, ", ".join(map(str, entry_ids)))
                    self._print_db(">> " + del_q)
                    cur = cur.execute(del_q)
                    # throw exception again (to be caught by the Databank program)
                    raise stop
                # execution was not stopped
                else:
                    # commit trace
                    commit()
                # for each new entry
                for (i, ins_cell) in ins_cells.items():
                    # for each input
                    for (input_, owner) in ins_cell.inputs.items():
                        # insert row-level input
                        inputs_q = "INSERT INTO \"{}_inputs_\" (entry, field, input, owner) VALUES ({}, NULL, '{}', {})" \
                                   .format(ast.table, i, input_, owner)
                        self._print_db(">> " + inputs_q)
                        cur = cur.execute(inputs_q)
                    # for each field
                    for (field, value) in ins_cell.value.items():
                        # for each field-level input
                        for (input_, owner) in value.inputs.items():
                            # insert input
                            inputs_q = "INSERT INTO \"{}_inputs_\" (entry, field, input, owner) VALUES ({}, '{}', '{}', {})" \
                                       .format(ast.table, i, field, input_, owner)
                            self._print_db(">> " + inputs_q)
                            cur = cur.execute(inputs_q)
                delete_new_q = "DELETE FROM \"{}_new_\"".format(ast.table)
                self._print_db(">> " + delete_new_q)
                cur = cur.execute(delete_new_q)
                return Cell(entry_ids, inputs=log_cell.inputs)
        elif isinstance(ast, sql.Delete):
            with self.db_cur() as cur:
                # select ids to be deleted
                ast_ids = sql.Select(result_columns=sql.ResultColumns(
                    type_="list", columns=[sql.Var(name="id")]),
                                     table=ast.table,
                                     where=ast.where)
                self._print_db(">> " + str(ast_ids))
                cur = cur.execute(str(ast_ids))
                ids = [i[0] for i in cur.fetchall()]
                self._print_db("<< " + repr(ids))
                # select inputs to be deleted
                inputs_ids_q = "SELECT id FROM \"{}_inputs_\" WHERE entry IN ({})" \
                               .format(ast.table, ", ".join(map(str, ids)))
                self._print_db(">> " + inputs_ids_q)
                cur = cur.execute(inputs_ids_q)
                inputs_ids = [i[0] for i in cur.fetchall()]
                self._print_db("<< " + repr(inputs_ids))
                log_cell = Cell(None, inputs=args.inputs)
                try:
                    lock()
                    # for each new entry
                    for i in inputs_ids:
                        # try to log deletion of the entry
                        # nothing to delete in case of Stop
                        log_cell.add_inputs(logdelete(self.id_, ast.table, i, stack.all(), assigned, called).inputs)
                except Stop as stop:
                    #reset()
                    pass
                else:
                    commit()
                # delete everything
                delete_q = "DELETE FROM \"{}\" WHERE id in ({})" \
                           .format(ast.table, ", ".join(map(str, ids)))
                self._print_db(">> " + delete_q)
                cur = cur.execute(delete_q)
                delete_inputs_q = "DELETE FROM \"{}_inputs_\" WHERE id in ({})" \
                                  .format(ast.table, ", ".join(map(str, inputs_ids)))
                self._print_db(">> " + delete_inputs_q)
                cur = cur.execute(delete_inputs_q)
                return Cell(ids, inputs=log_cell.inputs)
        else:
            assert(False)

    def add_sql_inputs(self, table, inputs):
        if not inputs:
            return
        # sanitize table
        logsanitize(self.id_, inputs, [table], [])
        table = f"{self.id_}_{table}"
        # insert input
        inputs_q = "INSERT INTO \"{}_inputs_\" (entry, field, input, owner) VALUES {}" \
                   .format(table, ", ".join([f"(NULL, NULL, '{input_}', {owner})" for (input_, owner) in inputs.items()]))
        self._print_db(">> " + inputs_q)
        with self.db_cur() as cur:
            cur = cur.execute(inputs_q)

    def get_sql_inputs(self, table):
        table = f"{self.id_}_{ast.table}"
        # retrieve inputs
        inputs_q = ("SELECT i.id, i.entry, i.input, i.owner FROM \"{}_inputs_\" AS i "
                    "WHERE i.entry IS NULL").format(table)
        self._print_db(">> " + inputs_q)
        with self.db_cur(select_only=True) as cur:
            cur = cur.execute(inputs_q)
            inputs = {i[3]: i[4] for i in cur.fetchall()}
        return inputs

    # Register inputs
    
    def register(self, func_name, key, value):
        return loginput(str(self.id_) + "/" + func_name, key, value, self._me(), self.now(), auto=True)

## Passive application wrapper
            
class PassiveApplication:

    def __init__(self, flask, server, id_, app_name, sp_IP, database, key, databank_side=True):
        self.flask = flask
        self.id_ = id_
        self.app_name = app_name
        if databank_side:
            self.server = server
        else:
            self.server = Server(databank_side=False)            
        self.server.register_app(id_, sp_IP, key)
        self.database = database
        self.aes = AES.new(bytes(key, 'utf8'), AES.MODE_EAX)
        self.databank_side = databank_side
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.cursor().execute("PRAGMA synchronous = OFF")
        self.lock = RLock()
        self.sql_asts = {}

    # Function decorators

    def callback(self, rule):
        def inner(f):
            def wrapper(*args, **kw):
                x = f(*args, **kw)
                return x
            wrapper.__name__ = str(self.id_) + "__" + f.__name__
            self.server.register_callback(self.id_, rule, self, wrapper)
            return wrapper
        return inner
    
    def route(self, rule, **kwargs):
        def inner(f):
            def wrapper(*args, **kw):
                x = f(*args, **kw)
                return x
            wrapper.__name__ = str(self.id_) + "__" + f.__name__
            return self.flask.route(join_route(self.id_, rule), **kwargs)(wrapper)
        return inner

    # Distant call

    def call(self, addr, function, *args, stack=None, assigned=None, **kwargs):
        dump = pickle.dumps((function, args.sanitize(), kwargs.sanitize()))
        msg = self.aes.encrypt(pad(dump))
        ret = do_call(msg, addr, databank_side=self.databank_side) 
        data = pickle.loads(self.aes.decrypt(ret).strip())
        return data

    # Exposed user input methods

    def method(self):
        return request.method

    def post(self, key):
        return request.form.get(key, None)

    def get(self, key):
        return request.args.get(key, None)

    # Session

    def get_session(self, key):
        if key in session and key[:4] != "user":
            cell = session[key]
            return cell
        else:
            return None

    def pop_session(self, key):
        if key in session and key[:4] != "user":
            session.pop(key, None)
        return None

    def set_session(self, key, value):
        session[key] = value.dump()
        return None

    # extension: COOKIES

    def _me(self):
        try:
            return session['user_id']
        except RuntimeError:
            # no active HTTP request → callback
            return self.callback_user_id
    
    def me(self):
        value = self._me()
        return value

    def name(self):
        try:
            value = session['user_name']
            return value
        except RuntimeError:
            # no active HTTP request → callback
            return self.callback_user_name

    # extension: access name and other personal information

    def now(self):
        return int(time.time())

    def now_utc(self):
        return datetime.utcfromtimestamp(self.now()).strftime('%Y-%m-%d @ %H:%M')
            
    # Database operations

    def db_cur(self, select_only=False):
        return Cur(self.db, self.lock, select_only=select_only)

    def _print_db(self, s):
        if is_set('verbose_db'):
            print(s)

    @timing('../evaluation/time.json', 'database')
    def sql(self, query, args=None, stack=None, assigned=None):
        print(query)
        if query in self.sql_asts:
            ast, select_only = deepcopy(self.sql_asts[query])
        else:
            ast = sql.parse(query)
            ast.table = f"{self.id_}_{ast.table}"
            if isinstance(ast, sql.Select):
                for join in ast.joins:
                    join.table = f"{self.id_}_{join.table}"
                select_only = True
            else:
                select_only = False
            self.sql_asts[query] = deepcopy(ast), select_only
        t2 = time.time()
        if args is not None:
            ast.set_params(args)
        with self.db_cur(select_only=select_only) as cur:
            self._print_db(">> " + str(ast))
            cur = cur.execute(str(ast))
            results = cur.fetchall()
            self._print_db("<< " + repr(results))
        t3 = time.time()
        return results
