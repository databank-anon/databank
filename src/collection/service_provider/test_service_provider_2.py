from databank.application import Application

app = Application(None, None, 1, "test", "127.0.0.1", None, "The answer is no", databank_side=False)

app.server.start()

print(app.call("127.0.0.1", "test"))


