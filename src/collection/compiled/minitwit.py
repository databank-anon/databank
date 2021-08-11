
from apps import minitwit
from databank.imports import *
__stack__ = None

def is_registered():
    global __stack__
    ___600 = minitwit.me()
    ___601 = minitwit.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([___600]))
    ___602 = db_len(___601)
    __r__ = Cell(Cell((___602 > Cell(0))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def user_exists(user_id):
    global __stack__
    ___603 = minitwit.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([user_id]))
    ___604 = db_len(___603)
    __r__ = Cell(Cell((___604 > Cell(0))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def make_page(title, body, flashed):
    global __stack__
    if ('html' not in locals()):
        html = Cell(None)
    html = ((Cell('<!doctype html>\n<title>') + title) + Cell(' | MiniTwit</title>\n<link rel=stylesheet type=text/css href="/static/css/minitwit.css">\n<div class=page>\n  <h1>MiniTwit</h1>\n  <div class=navigation>\n'))
    html.add_inputs(__stack__.all())
    try:
        ___605 = is_registered()[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        raise __stop__
    ___606 = ___605
    if ___606:
        __stack__.push()
        __stack__.add(___606.inputs)
        html = (html + Cell('    <a href="/3/timeline">my timeline</a> |\n    <a href="/3/public">public timeline</a>\n'))
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___606, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___606.inputs)
    if non(___606):
        __stack__.push()
        __stack__.add(___606.inputs)
        html = (html + Cell('    <a href="/3/public">public timeline</a> |\n    <a href="/3/register">sign up</a>\n'))
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___606, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___606.inputs)
    ___607 = Cell((flashed != Cell('')))
    if ___607:
        __stack__.push()
        __stack__.add(___607.inputs)
        html = (html + ((Cell('  </div>\n  <ul class=flashes>\n    <li>') + flashed) + Cell('\n  </ul>')))
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___607, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___607.inputs)
    html = (html + ((Cell('  <div class=body>\n  ') + body) + Cell('\n  <div class=footer>\n    MiniTwit &mdash; A Flask application\n  </div>')))
    html.add_inputs(__stack__.all())
    __r__ = Cell(html, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def get_public_timeline_messages():
    global __stack__
    if ('msgs_' not in locals()):
        msgs_ = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('msgs' not in locals()):
        msgs = Cell(None)
    ___608 = minitwit.sql(Cell('SELECT * FROM messages ORDER BY id DESC'))
    msgs = ___608
    msgs.add_inputs(__stack__.all())
    msgs_ = Cell([])
    msgs_.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___609 = db_len(msgs)
    ___610 = Cell((Cell((i < Cell(30))).value and Cell((i < ___609)).value), inputs=dict(Cell((i < Cell(30))).inputs))
    while ___610:
        __stack__.push()
        __stack__.add(___610.inputs)
        msgs_ = (msgs_ + Cell([msgs[i]]))
        msgs_.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___609 = db_len(msgs)
        ___610 = Cell((Cell((i < Cell(30))).value and Cell((i < ___609)).value), inputs=dict(Cell((i < Cell(30))).inputs))
    logsanitize(minitwit.id_, Cell(___610, adopt=__stack__.all()).inputs, [], [], auto=True)
    msgs_.add_inputs(__stack__.all())
    msgs_.add_inputs(___610.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___610.inputs)
    __r__ = Cell(msgs_, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def get_user_timeline_messages(user_id):
    global __stack__
    if ('msg_ids' not in locals()):
        msg_ids = Cell(None)
    if ('msg' not in locals()):
        msg = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('msg_id' not in locals()):
        msg_id = Cell(None)
    if ('msgs' not in locals()):
        msgs = Cell(None)
    ___611 = minitwit.sql(Cell('SELECT message FROM timeline WHERE user = ?0 ORDER BY id DESC'), Cell([user_id]))
    msg_ids = ___611
    msg_ids.add_inputs(__stack__.all())
    msgs = Cell([])
    msgs.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___612 = db_len(msg_ids)
    ___613 = Cell((Cell((i < Cell(30))).value and Cell((i < ___612)).value), inputs=dict(Cell((i < Cell(30))).inputs))
    while ___613:
        __stack__.push()
        __stack__.add(___613.inputs)
        msg_id = msg_ids[i][Cell(0)]
        msg_id.add_inputs(__stack__.all())
        ___614 = minitwit.sql(Cell('SELECT * FROM messages WHERE id = ?0'), Cell([msg_id]))
        msg = ___614[Cell(0)]
        msg.add_inputs(__stack__.all())
        msgs = (msgs + Cell([msg]))
        msgs.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___612 = db_len(msg_ids)
        ___613 = Cell((Cell((i < Cell(30))).value and Cell((i < ___612)).value), inputs=dict(Cell((i < Cell(30))).inputs))
    logsanitize(minitwit.id_, Cell(___613, adopt=__stack__.all()).inputs, [], [], auto=True)
    msg.add_inputs(__stack__.all())
    msg.add_inputs(___613.inputs)
    msg_id.add_inputs(__stack__.all())
    msg_id.add_inputs(___613.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___613.inputs)
    msgs.add_inputs(__stack__.all())
    msgs.add_inputs(___613.inputs)
    __r__ = Cell(msgs, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def add_message_to_user_timeline(user_id, message_id):
    global __stack__
    try:
        ___615 = minitwit.sql(Cell('INSERT INTO timeline (user, message) VALUES (?0, ?1)'), Cell([user_id, message_id]), stack=__stack__, assigned=['timeline'], called=[minitwit.me()])
    except Stop as __stop__:
        minitwit.add_sql_inputs('timeline', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___615.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

def push_message(author_id, text):
    global __stack__
    if ('new_ids' not in locals()):
        new_ids = Cell(None)
    ___616 = minitwit.now_utc()
    try:
        ___617 = minitwit.sql(Cell('INSERT INTO messages (author, text, datetime) VALUES (?0, ?1, ?2)'), Cell([author_id, text, ___616]), stack=__stack__, assigned=['messages'], called=[minitwit.me()])
    except Stop as __stop__:
        minitwit.add_sql_inputs('messages', __stop__.inputs)
        new_ids.add_inputs(__stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___617.inputs, bot=True)
    new_ids = ___617
    new_ids.add_inputs(__stack__.all())
    __r__ = Cell(new_ids[Cell(0)], adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def get_followees(user_id):
    global __stack__
    ___618 = minitwit.sql(Cell('SELECT follower FROM following WHERE followed = ?0'), Cell([user_id]))
    __r__ = Cell(___618, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def follow(user1, user2):
    global __stack__
    try:
        ___619 = minitwit.sql(Cell('INSERT INTO following (follower, followed) VALUES (?0, ?1)'), Cell([user1, user2]), stack=__stack__, assigned=['following'], called=[minitwit.me()])
    except Stop as __stop__:
        minitwit.add_sql_inputs('following', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___619.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

def unfollow(user1, user2):
    global __stack__
    try:
        ___620 = minitwit.sql(Cell('DELETE FROM following WHERE follower = ?0 AND followed = ?1'), Cell([user1, user2]), stack=__stack__, assigned=['following'], called=[minitwit.me()])
    except Stop as __stop__:
        minitwit.add_sql_inputs('following', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___620.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

def get_username(user_id):
    global __stack__
    ___621 = minitwit.sql(Cell('SELECT name FROM users WHERE id = ?0'), Cell([user_id]))
    __s__ = __stack__.all()
    return (None, __s__, [], [])

def timeline():
    global __stack__
    try:
        ___622 = timeline_(Cell(''))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___622, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/')
def _timeline():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = timeline()
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def timeline_(flash):
    global __stack__
    try:
        ___623 = is_registered()[0]
    except Stop as __stop__:
        raise __stop__
    ___624 = non(___623)
    if ___624:
        __stack__.push()
        __stack__.add(___624.inputs)
        try:
            ___625 = public_timeline()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___625, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___624, adopt=__stack__.all()).inputs, [], [], auto=True, u=minitwit.me())
        __stack__.add(___624.inputs, bot=True)
    ___626 = minitwit.me()
    try:
        ___627 = user_timeline_(___626, flash)[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___627, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def public_timeline():
    global __stack__
    try:
        ___628 = public_timeline_(Cell(''))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___628, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/public')
def _public_timeline():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = public_timeline()
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def public_timeline_(flash):
    global __stack__
    if ('body' not in locals()):
        body = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('username_' not in locals()):
        username_ = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('message' not in locals()):
        message = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('messages' not in locals()):
        messages = Cell(None)
    try:
        ___629 = get_public_timeline_messages()[0]
    except Stop as __stop__:
        username_.add_inputs(__stop__.inputs)
        title.add_inputs(__stop__.inputs)
        messages.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        message.add_inputs(__stop__.inputs)
        body.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        raise __stop__
    messages = ___629
    messages.add_inputs(__stack__.all())
    title = Cell('Public Timeline')
    title.add_inputs(__stack__.all())
    body = ((Cell('  <h2>') + title) + Cell('</h2>\n  <ul class=messages>'))
    body.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___630 = db_len(messages)
    L = ___630
    L.add_inputs(__stack__.all())
    ___631 = Cell((i < L))
    while ___631:
        __stack__.push()
        __stack__.add(___631.inputs)
        message = messages[i]
        message.add_inputs(__stack__.all())
        ___632 = minitwit.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([message[Cell(1)]]))
        username_ = ___632[Cell(0)][Cell(0)]
        username_.add_inputs(__stack__.all())
        body = (body + ((((((((Cell('    <li><p>\n      <strong><a href="/3/') + username_) + Cell('">')) + username_) + Cell('</a></strong>\n')) + message[Cell(2)]) + Cell('\n      <small>&mdash; ')) + message[Cell(3)]) + Cell('</small>\n')))
        body.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___631 = Cell((i < L))
    logsanitize(minitwit.id_, Cell(___631, adopt=__stack__.all()).inputs, [], [], auto=True)
    username_.add_inputs(__stack__.all())
    username_.add_inputs(___631.inputs)
    body.add_inputs(__stack__.all())
    body.add_inputs(___631.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___631.inputs)
    message.add_inputs(__stack__.all())
    message.add_inputs(___631.inputs)
    ___633 = Cell((L == Cell(0)))
    if ___633:
        __stack__.push()
        __stack__.add(___633.inputs)
        body = (body + Cell("    <li><em>There's no message so far.</em>\n  </ul>"))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___633, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___633.inputs)
    if non(___633):
        __stack__.push()
        __stack__.add(___633.inputs)
        body = (body + Cell('  </ul>\n'))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___633, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___633.inputs)
    try:
        ___634 = make_page(title, body, flash)[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___634, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def user_timeline(username):
    global __stack__
    if ('user_id' not in locals()):
        user_id = Cell(None)
    ___635 = minitwit.sql(Cell('SELECT id FROM users WHERE name = ?0'), Cell([username]))
    user_id = ___635[Cell(0)][Cell(0)]
    user_id.add_inputs(__stack__.all())
    try:
        ___636 = user_timeline_(user_id, Cell(''))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___636, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/<username>')
def _user_timeline(username):
    global __stack__
    __stack__ = Stack()
    username = minitwit.register('user_timeline', 'username', username)
    (__r__, __s__, __a__, __u__) = user_timeline(username)
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def user_timeline_(user_id, flash):
    global __stack__
    if ('body' not in locals()):
        body = Cell(None)
    if ('username' not in locals()):
        username = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('me_username' not in locals()):
        me_username = Cell(None)
    if ('me_user' not in locals()):
        me_user = Cell(None)
    if ('username_' not in locals()):
        username_ = Cell(None)
    if ('followed' not in locals()):
        followed = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('message' not in locals()):
        message = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('user' not in locals()):
        user = Cell(None)
    if ('messages' not in locals()):
        messages = Cell(None)
    ___637 = minitwit.sql(Cell('SELECT name FROM users WHERE id = ?0'), Cell([user_id]))
    user = ___637
    user.add_inputs(__stack__.all())
    ___638 = db_len(user)
    ___639 = Cell((___638 == Cell(0)))
    if ___639:
        __stack__.push()
        __stack__.add(___639.inputs)
        try:
            ___640 = timeline()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___640, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___639, adopt=__stack__.all()).inputs, [], [], auto=True, u=minitwit.me())
        __stack__.add(___639.inputs, bot=True)
    username_ = user[Cell(0)][Cell(0)]
    username_.add_inputs(__stack__.all())
    try:
        ___641 = get_user_timeline_messages(user_id)[0]
    except Stop as __stop__:
        title.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        me_username.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        username.add_inputs(__stop__.inputs)
        followed.add_inputs(__stop__.inputs)
        me_user.add_inputs(__stop__.inputs)
        message.add_inputs(__stop__.inputs)
        messages.add_inputs(__stop__.inputs)
        body.add_inputs(__stop__.inputs)
        raise __stop__
    messages = ___641
    messages.add_inputs(__stack__.all())
    title = (username_ + Cell("'s Timeline"))
    title.add_inputs(__stack__.all())
    try:
        ___642 = is_registered()[0]
    except Stop as __stop__:
        i.add_inputs(__stop__.inputs)
        me_username.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        username.add_inputs(__stop__.inputs)
        followed.add_inputs(__stop__.inputs)
        me_user.add_inputs(__stop__.inputs)
        message.add_inputs(__stop__.inputs)
        body.add_inputs(__stop__.inputs)
        raise __stop__
    ___643 = ___642
    if ___643:
        __stack__.push()
        __stack__.add(___643.inputs)
        ___644 = minitwit.me()
        ___645 = minitwit.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([___644]))
        me_username = ___645[Cell(0)][Cell(0)]
        me_username.add_inputs(__stack__.all())
        ___646 = minitwit.me()
        ___647 = minitwit.sql(Cell('SELECT * FROM following WHERE follower = ?0 AND followed = ?1'), Cell([___646, user_id]))
        ___648 = db_len(___647)
        followed = Cell((___648 > Cell(0)))
        followed.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___643, adopt=__stack__.all()).inputs, [], [], auto=True)
        followed.add_inputs(__stack__.all())
        followed.add_inputs(___643.inputs)
        me_username.add_inputs(__stack__.all())
        me_username.add_inputs(___643.inputs)
    if non(___643):
        __stack__.push()
        __stack__.add(___643.inputs)
        followed = Cell(False)
        followed.add_inputs(__stack__.all())
        me_user = Cell(None)
        me_user.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___643, adopt=__stack__.all()).inputs, [], [], auto=True)
        me_user.add_inputs(__stack__.all())
        me_user.add_inputs(___643.inputs)
        followed.add_inputs(__stack__.all())
        followed.add_inputs(___643.inputs)
    body = ((Cell('  <h2>') + title) + Cell('</h2>\n  <div class=followstatus>\n'))
    body.add_inputs(__stack__.all())
    ___649 = minitwit.me()
    ___650 = Cell((user_id == ___649))
    if ___650:
        __stack__.push()
        __stack__.add(___650.inputs)
        body = (body + Cell('      This is you!\n'))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___650, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___650.inputs)
    if non(___650):
        __stack__.push()
        __stack__.add(___650.inputs)
        ___651 = followed
        if ___651:
            __stack__.push()
            __stack__.add(___651.inputs)
            ___652 = db_str(user_id)
            body = (body + ((Cell('      You are currently following this user.\n      <a class=unfollow href="/3/') + ___652) + Cell('/unfollow">Unfollow user</a>.\n')))
            body.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(minitwit.id_, Cell(___651, adopt=__stack__.all()).inputs, [], [], auto=True)
            body.add_inputs(__stack__.all())
            body.add_inputs(___651.inputs)
        if non(___651):
            __stack__.push()
            __stack__.add(___651.inputs)
            ___653 = db_str(user_id)
            body = (body + ((Cell('      You are not yet following this user.\n      <a class=follow href="/3/') + ___653) + Cell('/follow">Follow user</a>.\n')))
            body.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(minitwit.id_, Cell(___651, adopt=__stack__.all()).inputs, [], [], auto=True)
            body.add_inputs(__stack__.all())
            body.add_inputs(___651.inputs)
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___650, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___650.inputs)
    body = (body + Cell('  </div>\n\n'))
    body.add_inputs(__stack__.all())
    ___654 = minitwit.me()
    ___655 = Cell((user_id == ___654))
    if ___655:
        __stack__.push()
        __stack__.add(___655.inputs)
        body = (body + ((Cell("  <div class=twitbox>\n    <h3>What's on your mind ") + username_) + Cell('?</h3>\n    <form action="/3/add_message" method=post>\n      <p><input type=text name=text size=60><!--\n      --><input type=submit value="Share">\n    </form>\n  </div>\n')))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___655, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___655.inputs)
    body = (body + Cell('  <ul class=messages>\n'))
    body.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___656 = db_len(messages)
    L = ___656
    L.add_inputs(__stack__.all())
    ___657 = Cell((i < L))
    while ___657:
        __stack__.push()
        __stack__.add(___657.inputs)
        message = messages[i]
        message.add_inputs(__stack__.all())
        ___658 = minitwit.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([message[Cell(1)]]))
        username = ___658[Cell(0)][Cell(0)]
        username.add_inputs(__stack__.all())
        body = (body + ((((((((Cell('    <li><p>\n      <strong><a href="/3/') + username) + Cell('">')) + username) + Cell('</a></strong>\n')) + message[Cell(2)]) + Cell('\n      <small>&mdash; ')) + message[Cell(3)]) + Cell('</small>\n')))
        body.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___657 = Cell((i < L))
    logsanitize(minitwit.id_, Cell(___657, adopt=__stack__.all()).inputs, [], [], auto=True)
    body.add_inputs(__stack__.all())
    body.add_inputs(___657.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___657.inputs)
    message.add_inputs(__stack__.all())
    message.add_inputs(___657.inputs)
    username.add_inputs(__stack__.all())
    username.add_inputs(___657.inputs)
    ___659 = Cell((L == Cell(0)))
    if ___659:
        __stack__.push()
        __stack__.add(___659.inputs)
        body = (body + Cell("    <li><em>There's no message so far.</em>\n  </ul>"))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___659, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___659.inputs)
    if non(___659):
        __stack__.push()
        __stack__.add(___659.inputs)
        body = (body + Cell('  </ul>\n'))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___659, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___659.inputs)
    try:
        ___660 = make_page(title, body, flash)[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___660, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def follow_user(user_id):
    global __stack__
    if ('username' not in locals()):
        username = Cell(None)
    try:
        ___661 = is_registered()[0]
    except Stop as __stop__:
        username.add_inputs(__stop__.inputs)
        minitwit.add_sql_inputs('following', __stop__.inputs)
        raise __stop__
    try:
        ___662 = user_exists(user_id)[0]
    except Stop as __stop__:
        username.add_inputs(__stop__.inputs)
        minitwit.add_sql_inputs('following', __stop__.inputs)
        raise __stop__
    ___663 = Cell((non(___661).value or non(___662).value), inputs=dict(non(___661).inputs))
    if ___663:
        __stack__.push()
        __stack__.add(___663.inputs)
        try:
            ___664 = timeline()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___664, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___663, adopt=__stack__.all()).inputs, [], [], auto=True, u=minitwit.me())
        __stack__.add(___663.inputs, bot=True)
    ___665 = minitwit.me()
    try:
        ___666 = follow(___665, user_id)[0]
    except Stop as __stop__:
        username.add_inputs(__stop__.inputs)
        minitwit.add_sql_inputs('following', __stop__.inputs)
        raise __stop__
    ___667 = minitwit.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([user_id]))
    username = ___667[Cell(0)][Cell(0)]
    username.add_inputs(__stack__.all())
    try:
        ___668 = user_timeline_(user_id, ((Cell('You are now following "') + username) + Cell("'")))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___668, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/<user_id>/follow')
def _follow_user(user_id):
    global __stack__
    __stack__ = Stack()
    user_id = minitwit.register('follow_user', 'user_id', user_id)
    (__r__, __s__, __a__, __u__) = follow_user(user_id)
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def unfollow_user(user_id):
    global __stack__
    if ('username' not in locals()):
        username = Cell(None)
    try:
        ___669 = is_registered()[0]
    except Stop as __stop__:
        minitwit.add_sql_inputs('following', __stop__.inputs)
        username.add_inputs(__stop__.inputs)
        raise __stop__
    try:
        ___670 = user_exists(user_id)[0]
    except Stop as __stop__:
        minitwit.add_sql_inputs('following', __stop__.inputs)
        username.add_inputs(__stop__.inputs)
        raise __stop__
    ___671 = Cell((non(___669).value or non(___670).value), inputs=dict(non(___669).inputs))
    if ___671:
        __stack__.push()
        __stack__.add(___671.inputs)
        try:
            ___672 = timeline()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___672, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___671, adopt=__stack__.all()).inputs, [], [], auto=True, u=minitwit.me())
        __stack__.add(___671.inputs, bot=True)
    ___673 = minitwit.me()
    try:
        ___674 = unfollow(___673, user_id)[0]
    except Stop as __stop__:
        minitwit.add_sql_inputs('following', __stop__.inputs)
        username.add_inputs(__stop__.inputs)
        raise __stop__
    ___675 = minitwit.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([user_id]))
    username = ___675[Cell(0)][Cell(0)]
    username.add_inputs(__stack__.all())
    try:
        ___676 = user_timeline_(user_id, ((Cell('You are no longer following "') + username) + Cell("'")))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___676, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/<user_id>/unfollow')
def _unfollow_user(user_id):
    global __stack__
    __stack__ = Stack()
    user_id = minitwit.register('unfollow_user', 'user_id', user_id)
    (__r__, __s__, __a__, __u__) = unfollow_user(user_id)
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_message():
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('followers' not in locals()):
        followers = Cell(None)
    if ('message_id' not in locals()):
        message_id = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    ___677 = minitwit.post('add_message', Cell('text'))
    ___678 = ___677
    if ___678:
        __stack__.push()
        __stack__.add(___678.inputs)
        ___679 = minitwit.me()
        ___680 = minitwit.post('add_message', Cell('text'))
        try:
            ___681 = push_message(___679, ___680)[0]
        except Stop as __stop__:
            message_id.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            minitwit.add_sql_inputs('timeline', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            followers.add_inputs(__stop__.inputs)
            raise __stop__
        message_id = ___681
        message_id.add_inputs(__stack__.all())
        ___682 = minitwit.me()
        try:
            ___683 = add_message_to_user_timeline(___682, message_id)[0]
        except Stop as __stop__:
            i.add_inputs(__stop__.inputs)
            minitwit.add_sql_inputs('timeline', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            followers.add_inputs(__stop__.inputs)
            raise __stop__
        ___684 = minitwit.me()
        ___685 = minitwit.sql(Cell('SELECT follower FROM following WHERE followed = ?0'), Cell([___684]))
        followers = ___685
        followers.add_inputs(__stack__.all())
        ___686 = db_len(followers)
        L = ___686
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___687 = Cell((i < L))
        while ___687:
            __stack__.push()
            __stack__.add(___687.inputs)
            try:
                ___688 = add_message_to_user_timeline(followers[i][Cell(0)], message_id)[0]
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                minitwit.add_sql_inputs('timeline', __stop__.inputs)
                raise __stop__
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___687 = Cell((i < L))
        logsanitize(minitwit.id_, Cell(___687, adopt=__stack__.all()).inputs, [], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___687.inputs)
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___678, adopt=__stack__.all()).inputs, [], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___678.inputs)
        message_id.add_inputs(__stack__.all())
        message_id.add_inputs(___678.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___678.inputs)
        followers.add_inputs(__stack__.all())
        followers.add_inputs(___678.inputs)
    try:
        ___689 = timeline_(Cell('Your message was recorded'))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___689, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/add_message', methods=['POST'])
def _add_message():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = add_message()
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def register():
    global __stack__
    try:
        ___690 = register_(Cell(None))[0]
    except Stop as __stop__:
        minitwit.add_sql_inputs('users', __stop__.inputs)
        raise __stop__
    __r__ = Cell(___690, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@minitwit.route('/register', methods=['GET', 'POST'])
def _register():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = register()
    logreturn(minitwit.id_, minitwit.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def register_(error):
    global __stack__
    if ('body' not in locals()):
        body = Cell(None)
    if ('username' not in locals()):
        username = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('email' not in locals()):
        email = Cell(None)
    try:
        ___691 = is_registered()[0]
    except Stop as __stop__:
        title.add_inputs(__stop__.inputs)
        body.add_inputs(__stop__.inputs)
        email.add_inputs(__stop__.inputs)
        minitwit.add_sql_inputs('users', __stop__.inputs)
        error.add_inputs(__stop__.inputs)
        username.add_inputs(__stop__.inputs)
        raise __stop__
    ___692 = ___691
    if ___692:
        __stack__.push()
        __stack__.add(___692.inputs)
        try:
            ___693 = timeline()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___693, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___692, adopt=__stack__.all()).inputs, [], [], auto=True, u=minitwit.me())
        __stack__.add(___692.inputs, bot=True)
    error = Cell(None)
    error.add_inputs(__stack__.all())
    title = Cell('Sign Up')
    title.add_inputs(__stack__.all())
    ___694 = minitwit.method()
    ___695 = Cell((___694 != Cell('POST')))
    if ___695:
        __stack__.push()
        __stack__.add(___695.inputs)
        error = Cell('')
        error.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___695, adopt=__stack__.all()).inputs, ['users'], [], auto=True, u=minitwit.me())
        __stack__.add(___695.inputs, bot=True)
        error.add_inputs(__stack__.all())
        error.add_inputs(___695.inputs)
    if non(___695):
        __stack__.push()
        __stack__.add(___695.inputs)
        ___696 = minitwit.post('register_', Cell('username'))
        ___697 = non(___696)
        if ___697:
            __stack__.push()
            __stack__.add(___697.inputs)
            error = Cell('You have to enter a username')
            error.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(minitwit.id_, Cell(___697, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
            error.add_inputs(__stack__.all())
            error.add_inputs(___697.inputs)
        if non(___697):
            __stack__.push()
            __stack__.add(___697.inputs)
            ___698 = minitwit.post('register_', Cell('email'))
            ___699 = minitwit.post('register_', Cell('email'))
            ___700 = Cell((non(___698).value or Cell((Cell('@') not in ___699)).value), inputs=dict(non(___698).inputs))
            if ___700:
                __stack__.push()
                __stack__.add(___700.inputs)
                error = Cell('You have to enter a valid email address')
                error.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(minitwit.id_, Cell(___700, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
                error.add_inputs(__stack__.all())
                error.add_inputs(___700.inputs)
            if non(___700):
                __stack__.push()
                __stack__.add(___700.inputs)
                ___701 = minitwit.post('register_', Cell('username'))
                try:
                    ___702 = user_exists(___701)[0]
                except Stop as __stop__:
                    body.add_inputs(__stop__.inputs)
                    email.add_inputs(__stop__.inputs)
                    minitwit.add_sql_inputs('users', __stop__.inputs)
                    error.add_inputs(__stop__.inputs)
                    username.add_inputs(__stop__.inputs)
                    raise __stop__
                ___703 = ___702
                if ___703:
                    __stack__.push()
                    __stack__.add(___703.inputs)
                    error = Cell('The username is already taken')
                    error.add_inputs(__stack__.all())
                    __stack__.pop()
                else:
                    logsanitize(minitwit.id_, Cell(___703, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
                    error.add_inputs(__stack__.all())
                    error.add_inputs(___703.inputs)
                if non(___703):
                    __stack__.push()
                    __stack__.add(___703.inputs)
                    ___704 = minitwit.me()
                    ___705 = minitwit.post('register_', Cell('username'))
                    ___706 = minitwit.post('register_', Cell('email'))
                    try:
                        ___707 = minitwit.sql(Cell('INSERT INTO users (user_id, name, email) VALUES (?0, ?1, ?2)'), Cell([___704, ___705, ___706]), stack=__stack__, assigned=['users'], called=[minitwit.me()])
                    except Stop as __stop__:
                        minitwit.add_sql_inputs('users', __stop__.inputs)
                        raise __stop__
                    else:
                        __stack__.add(___707.inputs, bot=True)
                    try:
                        ___708 = timeline_(Cell('You were successfully registered and can login now'))[0]
                    except Stop as __stop__:
                        raise __stop__
                    __r__ = Cell(___708, adopt=__stack__.all())
                    __s__ = __stack__.all()
                    __stack__.pop()
                    __stack__.pop()
                    __stack__.pop()
                    __stack__.pop()
                    return (__r__, __s__, [], [])
                    __stack__.pop()
                else:
                    logsanitize(minitwit.id_, Cell(___703, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
                    minitwit.add_sql_inputs('users', __stack__.all())
                    minitwit.add_sql_inputs('users', ___703.inputs)
                __stack__.pop()
            else:
                logsanitize(minitwit.id_, Cell(___700, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
                minitwit.add_sql_inputs('users', __stack__.all())
                minitwit.add_sql_inputs('users', ___700.inputs)
                error.add_inputs(__stack__.all())
                error.add_inputs(___700.inputs)
            __stack__.pop()
        else:
            logsanitize(minitwit.id_, Cell(___697, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
            minitwit.add_sql_inputs('users', __stack__.all())
            minitwit.add_sql_inputs('users', ___697.inputs)
            error.add_inputs(__stack__.all())
            error.add_inputs(___697.inputs)
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___695, adopt=__stack__.all()).inputs, ['users'], [], auto=True, u=minitwit.me())
        __stack__.add(___695.inputs, bot=True)
        minitwit.add_sql_inputs('users', __stack__.all())
        minitwit.add_sql_inputs('users', ___695.inputs)
        error.add_inputs(__stack__.all())
        error.add_inputs(___695.inputs)
    ___709 = minitwit.post('register_', Cell('username'))
    username = Cell((___709.value or Cell('').value), inputs=dict(___709.inputs))
    username.add_inputs(__stack__.all())
    ___710 = minitwit.post('register_', Cell('email'))
    email = Cell((___710.value or Cell('').value), inputs=dict(___710.inputs))
    email.add_inputs(__stack__.all())
    body = Cell('  <h2>Sign Up</h2>\n')
    body.add_inputs(__stack__.all())
    ___711 = Cell((error != Cell('')))
    if ___711:
        __stack__.push()
        __stack__.add(___711.inputs)
        body = (body + ((Cell('  <div class=error><strong>Error:</strong> ') + error) + Cell('</div>')))
        body.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(minitwit.id_, Cell(___711, adopt=__stack__.all()).inputs, [], [], auto=True)
        body.add_inputs(__stack__.all())
        body.add_inputs(___711.inputs)
    body = (body + ((((Cell('  <form action="" method=post>\n    <dl>\n      <dt>Username:\n      <dd><input type=text name=username size=30 value="') + username) + Cell('">\n      <dt>E-Mail:\n      <dd><input type=text name=email size=30 value="')) + email) + Cell('">\n    </dl>\n    <div class=actions><input type=submit value="Sign Up"></div>\n  </form>')))
    body.add_inputs(__stack__.all())
    try:
        ___712 = make_page(title, body, Cell(''))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___712, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])
