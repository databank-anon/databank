from flask import Flask, g
from flask_hashing import Hashing
import sqlite3
from os.path import join

from databank.calls import Server

## Files

TEMP_POLICY = join("..", "temp", "policy-{}")
MONPOLY     = join("..", "monpoly", "monpoly")
MONITOR_DIR = join("..", "monitor_files")
POLICY      = join(MONITOR_DIR, "policy-{}")
STATE       = join(MONITOR_DIR, "state-{}")
SIG         = join(MONITOR_DIR, "databank.sig")
TO_MONITOR  = [join("..", "db", "database.db")]

## Application

bank = Flask("The Databank")
bank.secret_key = "E4kB3BUlTXivYtkaKnCb9XHGIr9erSEIX0n0MWOnAqlqr2PGKWjPgWp2834M5PmDqx2dEvI2EV7YdriY"
hashing = Hashing(bank)
server = Server()

## Fundamental database

FUNDAMENTAL = join("..", "db", "fundamental.db")

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._database = sqlite3.connect(FUNDAMENTAL)
    return db

@bank.teardown_appcontext
def close_db(ex):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

## Options set by main
options = {}

def set_option(o, v=True):
    options[o] = v

def is_set(o):
    return options.get(o, False)
