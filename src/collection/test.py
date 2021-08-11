from apps import test

@test.route('hello/<int:uid>')
def hello(uid):
    msg = "Hi"
    name = test.sql("SELECT name FROM users WHERE uid = ?0", [uid])[0][0]
    if name != "":
        msg = msg + ", " + name
    return msg
