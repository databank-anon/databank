from settings import bank, server, is_set

from databank.application import Application, PassiveApplication

if is_set("passive"):
    ApplicationClass = PassiveApplication
else:
    ApplicationClass = Application

test = ApplicationClass(bank, server, 1, "Test", "127.0.0.1", "../db/database.db", "The answer is no")
meet = ApplicationClass(bank, server, 2, "Meet", "127.0.0.1", "../db/database.db", "The answer is no")
minitwit = ApplicationClass(bank, server, 3, "Minitwit", "127.0.0.1", "../db/database.db", "The answer is no")
