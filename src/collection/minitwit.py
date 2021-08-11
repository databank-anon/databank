from apps import minitwit

def is_registered():
    return len(minitwit.sql("SELECT * FROM users WHERE user_id = ?0", [minitwit.me()])) > 0

def user_exists(user_id):
    return len(minitwit.sql("SELECT * FROM users WHERE user_id = ?0", [user_id])) > 0

def make_page(title, body, flashed):
    html = """<!doctype html>
<title>""" + title + """ | MiniTwit</title>
<link rel=stylesheet type=text/css href="/static/css/minitwit.css">
<div class=page>
  <h1>MiniTwit</h1>
  <div class=navigation>
"""
    if is_registered():
        html += """    <a href="/3/timeline">my timeline</a> |
    <a href="/3/public">public timeline</a>
"""
    else:
        html += """    <a href="/3/public">public timeline</a> |
    <a href="/3/register">sign up</a>
"""
    if flashed != '':
        html += """  </div>
  <ul class=flashes>
    <li>""" + flashed + """
  </ul>"""
    html += """  <div class=body>
  """ + body + """
  <div class=footer>
    MiniTwit &mdash; A Flask application
  </div>"""
    return html

    
def get_public_timeline_messages():
    """Get public timeline message list."""
    msgs = minitwit.sql("SELECT * FROM messages ORDER BY id DESC")
    msgs_ = []
    i = 0
    while i < 30 and i < len(msgs):
        msgs_ += [msgs[i]]
        i += 1
    return msgs_


def get_user_timeline_messages(user_id):
    """Get user time line message list."""
    msg_ids = minitwit.sql("SELECT message FROM timeline WHERE user = ?0 ORDER BY id DESC",
                         [user_id])
    msgs = []
    i = 0
    while i < 30 and i < len(msg_ids):
        msg_id = msg_ids[i][0]
        msg = minitwit.sql("SELECT * FROM messages WHERE id = ?0", [msg_id])[0]
        msgs += [msg]
        i += 1
    return msgs


def add_message_to_user_timeline(user_id, message_id):
    """Add message id to user timeline messages list."""
    minitwit.sql("INSERT INTO timeline (user, message) VALUES (?0, ?1)", [user_id, message_id])

    
def push_message(author_id, text):
    """Add message and return its id."""
    new_ids = minitwit.sql("INSERT INTO messages (author, text, datetime) VALUES (?0, ?1, ?2)",
                           [author_id, text, minitwit.now_utc()])
    return new_ids[0]

    
def get_followees(user_id):
    """Get list of user followers."""
    return minitwit.sql("SELECT follower FROM following WHERE followed = ?0", [user_id])


def follow(user1, user2):
    """Follow the specified user."""
    minitwit.sql("INSERT INTO following (follower, followed) VALUES (?0, ?1)", [user1, user2])


def unfollow(user1, user2):
    """Unfollow the specified user."""
    minitwit.sql("DELETE FROM following WHERE follower = ?0 AND followed = ?1", [user1, user2])


def get_username(user_id):
    minitwit.sql("SELECT name FROM users WHERE id = ?0", [user_id])[0][0]


@minitwit.route('/')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    return timeline_('')


def timeline_(flash):
    if not is_registered():
        return public_timeline()
    return user_timeline_(minitwit.me(), flash)


@minitwit.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    return public_timeline_('')


def public_timeline_(flash):
    messages = get_public_timeline_messages()
    title = "Public Timeline"
    body = "  <h2>" + title + """</h2>
  <ul class=messages>"""
    i = 0
    L = len(messages)
    while i < L:
        message = messages[i]
        username_ = minitwit.sql("SELECT name FROM users WHERE user_id = ?0", [message[1]])[0][0]
        body += """    <li><p>
      <strong><a href="/3/""" + username_ + "\">" + username_ + """</a></strong>
""" + message[2] + """
      <small>&mdash; """ + message[3] + """</small>
"""
        i += 1
    if L == 0:
        body += """    <li><em>There's no message so far.</em>
  </ul>"""
    else:
        body += """  </ul>
"""
    return make_page(title, body, flash)


@minitwit.route('/<username>')
def user_timeline(username):
    """Displays a user's tweets."""
    user_id = minitwit.sql("SELECT id FROM users WHERE name = ?0", [username])[0][0]
    return user_timeline_(user_id, '')
    

def user_timeline_(user_id, flash):
    user = minitwit.sql("SELECT name FROM users WHERE id = ?0", [user_id])
    if len(user) == 0:
        return timeline()
    username_ = user[0][0]
    messages = get_user_timeline_messages(user_id)
    title = username_ + "'s Timeline"
    if is_registered():
        me_username = minitwit.sql("SELECT name FROM users WHERE user_id = ?0", [minitwit.me()])[0][0]
        followed = len(minitwit.sql("SELECT * FROM following WHERE follower = ?0 AND followed = ?1",
                                    [minitwit.me(), user_id])) > 0
    else:
        followed = False
        me_user = None
    body = "  <h2>" + title + """</h2>
  <div class=followstatus>
"""
    if user_id == minitwit.me():
        body += """      This is you!
"""
    elif followed:
        body += """      You are currently following this user.
      <a class=unfollow href="/3/""" + str(user_id) + """/unfollow">Unfollow user</a>.
"""
    else:
        body += """      You are not yet following this user.
      <a class=follow href="/3/""" + str(user_id) + """/follow">Follow user</a>.
"""
    body += """  </div>

"""
    if user_id == minitwit.me():
        body += """  <div class=twitbox>
    <h3>What's on your mind """ + username_ + """?</h3>
    <form action="/3/add_message" method=post>
      <p><input type=text name=text size=60><!--
      --><input type=submit value="Share">
    </form>
  </div>
"""
    body += """  <ul class=messages>
"""
    i = 0
    L = len(messages)
    while i < L:
        message = messages[i]
        username = minitwit.sql("SELECT name FROM users WHERE user_id = ?0", [message[1]])[0][0]
        body += """    <li><p>
      <strong><a href="/3/""" + username + "\">" + username + """</a></strong>
""" + message[2] + """
      <small>&mdash; """ + message[3] + """</small>
"""
        i += 1
    if L == 0:
        body += """    <li><em>There's no message so far.</em>
  </ul>"""
    else:
        body += """  </ul>
"""
    return make_page(title, body, flash)


@minitwit.route('/<user_id>/follow')
def follow_user(user_id):
    """Adds the current user as follower of the given user."""
    if not is_registered() or not user_exists(user_id):
        return timeline()
    follow(minitwit.me(), user_id)
    username = minitwit.sql("SELECT name FROM users WHERE user_id = ?0", [user_id])[0][0]
    return user_timeline_(user_id, 'You are now following "' + username + "'")


@minitwit.route('/<user_id>/unfollow')
def unfollow_user(user_id):
    """Removes the current user as follower of the given user."""
    if not is_registered() or not user_exists(user_id):
        return timeline()
    unfollow(minitwit.me(), user_id)
    username = minitwit.sql("SELECT name FROM users WHERE user_id = ?0", [user_id])[0][0]
    return user_timeline_(user_id, 'You are no longer following "' + username + "'")


@minitwit.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user."""
    if minitwit.post('text'):
        message_id = push_message(minitwit.me(), minitwit.post('text'))
        add_message_to_user_timeline(minitwit.me(), message_id)
        followers = minitwit.sql("SELECT follower FROM following WHERE followed = ?0",
                                 [minitwit.me()])
        L = len(followers)
        i = 0
        while i < L:
            add_message_to_user_timeline(followers[i][0], message_id)
            i += 1
    return timeline_('Your message was recorded')


@minitwit.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    return register_(None)
    

def register_(error):
    if is_registered():
        return timeline()
    error = None
    title = "Sign Up"
    if minitwit.method() != 'POST':
        error = ''
    elif not minitwit.post('username'):
        error = 'You have to enter a username'
    elif not minitwit.post('email') or \
         '@' not in minitwit.post('email'):
        error = 'You have to enter a valid email address'
    elif user_exists(minitwit.post('username')):
        error = 'The username is already taken'
    else:
        minitwit.sql("INSERT INTO users (user_id, name, email) VALUES (?0, ?1, ?2)",
                     [minitwit.me(), minitwit.post('username'), minitwit.post('email')])
        return timeline_('You were successfully registered and can login now')
    username = minitwit.post('username') or ""
    email = minitwit.post('email') or ""
    body = """  <h2>Sign Up</h2>
"""
    if error != '':
        body += "  <div class=error><strong>Error:</strong> " + error + "</div>"
    body += """  <form action="" method=post>
    <dl>
      <dt>Username:
      <dd><input type=text name=username size=30 value=\"""" + username + """\">
      <dt>E-Mail:
      <dd><input type=text name=email size=30 value=\"""" + email + """\">
    </dl>
    <div class=actions><input type=submit value="Sign Up"></div>
  </form>"""
    return make_page(title, body, '')
