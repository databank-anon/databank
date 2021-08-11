from flask import session
import sqlite3
from threading import RLock
from subprocess import Popen, PIPE, STDOUT
from settings import *
from databank.memory import Cell
from databank.timing import timing
import sqlite3
import os
import re
import hashlib
import time

# Printing function

def _print_monitor(s, end='\n'):
    if is_set('verbose_monitor'):
        print(s, end=end)

trace = ""

def _trace(s, i):
    global trace
    if is_set('trace'):
        trace += f"[{i}] {s}\n"
    return s

# (v, u) -> "v:u"

def _str_of_label(w):
    return str(w[0]) + ":" + str(w[1])

# "v:u" -> (v, u)

def _label_of_str(s):
    s = s.split(":")
    return s[0], int(s[1])

# hash if longer than 64 chars

def _shorten(o):
    try:
        r = str(o)
        assert len(r) <= 64
        return r.replace("\"", "'")
    except:
        return hashlib.sha256(repr(r).encode('utf-8')).hexdigest()
    
# Stop execution

class Stop(Exception):
    def __init__(self, user_id, inputs):
        self.user_id = user_id
        self.inputs  = inputs

# Predicates

class Inputs:

    sig = "Inputs(string,string,string,string)"
    
    def __init__(self, a, f, m, v):
        self.a = a
        self.f = f
        self.m = m
        self.v = v

    def __str__(self):
        return f"Inputs(\"{self.a}\", {self.f}, {self.m}, \"{_shorten(self.v)}\")"

class Learns:

    sig = "Learns(string,string)"
    
    def __init__(self, u, m):
        self.u = u
        self.m = m

    def __str__(self):
        return f"Learns({self.u}, {self.m})"

class Insert:

    sig = "Insert(string,int)"
    
    def __init__(self, i, k):
        self.i = i
        self.k = k

    def __str__(self):
        return f"Insert({self.i}, {self.k})"

class Delete:

    sig = "Delete(string,int)"
    
    def __init__(self, i, k):
        self.i = i
        self.k = k

    def __str__(self):
        return f"Delete({self.i}, {self.k})"

class Field:

    sig = "Field(string,int,string,string)"
    
    def __init__(self, i, k, f, x):
        self.i = i
        self.k = k
        self.f = f
        self.x = x

    def __str__(self):
        j = list(map(_str_of_label, self.x.inputs.items()))
        value = str(self.x.value).replace("\"", "'")
        s = f"Field({self.i}, {self.k}, {self.f}, \"{value}\""
        if j:
            s += " [" + ', '.join(j) + "])"
        else:
            s += ")"
        return s

# Single-user monitor

class Monitor:
    def __init__(self, user_id, policy):
        self.user_id = user_id
        self.policy = policy
        self.policy_fn = POLICY.format(user_id)
        with open(self.policy_fn, "w") as f:
            f.write(policy)
        self.state_fn = STATE.format(user_id)
        self.sig_fn = SIG
        self.unsaved = False
        if os.path.isfile(self.state_fn):
            self.resume()
        else:
            cmd = [MONPOLY, "-formula", self.policy_fn, "-sig", self.sig_fn, "-verbose", "-labels"]
            self.proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
            self._read_first_input()

    def _read_first_input(self):
        out = self.proc.stdout.readline()
        for _ in range(4 if "input formula" in out else 2):
            self.proc.stdout.readline()

    def tp(self):
        return int(time.time())

    def stop(self):
        self.save()
        self.proc.kill()

    RTRUE = re.compile(r"^@\d+\. \(time point \d+\): true")
    RFALSE = re.compile(r"^@\d+\. \(time point \d+\): false")
    RLABELS = re.compile(r"\[((?:[\:\w]+)(?:,[\:\w]+)*)\]")
        
    def log(self, pred, inputs=None):
        if is_set("semipassive"):
            return {}
        self.unsaved = True
        req = f"@{self.tp()} {pred} "
        if inputs:
            req += "[{}] > nop <".format(", ".join(map(_str_of_label, inputs.items())))
        else:
            req += "> nop <"
        _print_monitor(f"{self.user_id}→ {req}")
        self.proc.stdin.write(_trace(req, self.user_id))
        self.proc.stdin.flush()
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")
        out = self.proc.stdout.readline()
        _print_monitor(f"{self.user_id}← {out}", end="")
        olabs = Monitor.RLABELS.search(out)
        if olabs:
            labels = [_label_of_str(l) for l in olabs.group(1).split(", ")]
            labels = {v: u for (v, u) in labels}
        else:
            labels = {}
        _print_monitor(f"{self.user_id}← {out}", end="")
        if Monitor.RTRUE.match(out):
            self.resume()
            raise Stop(self.user_id, labels)
        else:
            try:
                assert(Monitor.RFALSE.match(out))
            except AssertionError as e:
                if is_set('trace'):
                    print("Monitoring trace dump:")
                    print(trace)
                raise e
            return labels

    def sanitize_table(self, id_, table, inputs):
        if is_set("semipassive") or not inputs:
            return
        self.unsaved = True
        req = """@{2} Insert ({0}, Null [{1}]) 
      Delete ({0}, Null [{1}])
      Field ({0}, Null [{1}], Null [{1}], Null [{1}]) > nop <""" \
          .format(f"{id_}_{table}", ", ".join(map(_str_of_label, inputs.items())), self.tp())
        _print_monitor(f"{self.user_id}→ {req}")
        self.proc.stdin.write(_trace(req, self.user_id))
        self.proc.stdin.flush()
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")

    def sanitize_user(self, user, inputs):
        if is_set("semipassive") or not inputs:
            return
        self.unsaved = True
        req = "@{} Learns ({}, Null [{}]) > nop <".format(
            self.tp(), _shorten(user.value), ", ".join(map(_str_of_label, inputs.items())))
        _print_monitor(f"{self.user_id}→ {req}")
        self.proc.stdin.write(_trace(req, self.user_id))
        self.proc.stdin.flush()
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")

    def save(self):
        if self.unsaved:
            req = f"> save_state {self.state_fn} <"
            _print_monitor(f"{self.user_id}→ {req}")
            self.proc.stdin.write(_trace(req, self.user_id))
            self.proc.stdin.flush()
            _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")
            self.unsaved = False

    def resume(self):
        cmd = [MONPOLY, "-formula", self.policy_fn, "-sig", self.sig_fn,
               "-load", self.state_fn, "-verbose", "-labels"]
        _print_monitor(f"{self.user_id}→ {' '.join(cmd)}")
        self.proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
        self._read_first_input()
        _print_monitor(f"{self.user_id}← {self.proc.stdout.readline()}", end="")

# Load monitors

monitors = {}

_db  = sqlite3.connect(FUNDAMENTAL)
_cur = _db.execute("SELECT id, policy FROM users")
_res = _cur.fetchall()
_cur.close()
_db.close()

for _r in _res:
    monitors[_r[0]] = Monitor(*_r)

with open(SIG, 'w') as f:
    f.write(Inputs.sig + "\n")
    f.write(Learns.sig + "\n")

_monitor_files = [f for f in os.listdir(MONITOR_DIR) \
                  if f.split('-')[0] == "state" and int(f.split('-')[1]) not in monitors]
for _monitor_file in _monitor_files:
    os.remove(os.path.join(MONITOR_DIR, _monitor_file))
        
# Monitor control functions (used by applications)

general_lock = RLock()

def _filter_labels(labels, id):
    return {l: u for (l, u) in labels.items() if u == id}

def loginsert(id_, t, k, c, j, A, U, auto=False):
    ###
    return Cell(None)
    ###
    if auto:
        lock()
    ret_cell = Cell(None, inputs=j)
    try:
        for monitor in monitors.values():
            ret_cell.add_inputs(monitor.log(Insert(t, k), inputs=j))
            for f, x in c.value.items():
                ret_cell.add_inputs(monitor.log(Field(t, k, f, x), inputs=j))
    except Stop as stop:
        logsanitize(id_, ret_cell.inputs, A, U, auto=False)
        if auto:
            commit()
        raise stop
    logsanitize(id_, ret_cell.inputs, A, U, auto=False)
    if auto:
        commit()
    return ret_cell

def logdelete(id_, t, k, j, A, U, auto=False):
    ###
    return Cell(None)
    ###
    if auto:
        lock()
    ret_cell = Cell(None, inputs=j)
    try:
        for monitor in monitors.values():
            ret_cell.add_inputs(monitor.log(Delete(t, k), inputs=j))
    except Stop as stop:
        logsanitize(id_, ret_cell.inputs, A, U, auto=False)
        if auto:
            commit()
        raise stop
    logsanitize(id_, ret_cell.inputs, A, U, auto=False)
    if auto:
        commit()
    return ret_cell

@timing('../evaluation/time.json', 'monitoring')
def logreturn(id_, u, c, j, A, U, auto=False):
    if auto:
        lock()
    users = {}
    if c is not None:
        for k, v in c.inputs.items():
            if v not in users:
                users[v] = set()
            users[v].add(k)
    ret_cell = Cell(None, inputs=j)
    old_ret_cell = set()
    while ret_cell.inputs != old_ret_cell:
        old_ret_cell = dict(ret_cell.inputs)
        try:
            for user, inputs in users.items():
                monitor = monitors[user]
                for input_ in inputs:
                    ret_cell.add_inputs(monitor.log(Learns(str(u.value), input_), inputs=old_ret_cell))
                monitor.sanitize_user(Cell(user), {input_: user for input_ in inputs})
        except Stop as stop:
            logsanitize(id_, ret_cell.inputs, A, U, auto=False, u=u)
            if auto:
                commit()
            raise stop
    logsanitize(id_, ret_cell.inputs, A, U, auto=False, u=u)
    if auto:
        commit()
    return ret_cell

@timing('../evaluation/time.json', 'monitoring')
def loginput(f, a, v, u, ts, auto=False):
    if auto:
        lock()
    i = hashlib.sha256((repr(f) + repr(a) + repr(v) + repr(u) + repr(ts)).encode('utf-8')).hexdigest()
    h = _shorten(v)
    monitors[u].log(Inputs(f, a, i, h))
    if auto:
        commit()
    return Cell(v, {i: u})

@timing('../evaluation/time.json', 'monitoring')        
def logsanitize(id_, j, A, U, auto=False, u=None):
    if not U and not u:
        return
    if auto:
        lock()
    users = {}
    for k, v in j.items():
        if v not in users:
            users[v] = set()
        users[v].add(k)
    for v, i in users.items():
        monitor = monitors[v]
        for w in U:
            monitor.sanitize_user(w, {ii: w.value for ii in i})
        if u is not None:
            monitor.sanitize_user(u, {ii: u.value for ii in i})
    #for monitor in monitors.values():
        #for a in A:
            #monitor.sanitize_table(id_, a, j)
        #for v in U:
            #monitor.sanitize_user(v, j)
        #if u is not None:
            #monitor.sanitize_user(u, j)
    if auto:
        commit()

def lock():
    for monitor in monitors.values():
        monitor.save()
    general_lock.acquire()

def commit():
    general_lock.release()
