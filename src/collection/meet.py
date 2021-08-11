from apps import meet

def make_page(html):
    return """<!doctype html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        
    <title>The Databank</title>
  </head>
  <body>
    <header class="navbar navbar-light" id="navbar">
      <div class="container-fluid">
        <a class="navbar-brand" href="/2">
          Meet
        </a>
      </div>
    </header>
    <div class="container">
      <div class="row">
        <div class="col-sm-8 offset-sm-2">
           <div class="card">
""" + html + """
           </div>
        </div>
        <div class="col-sm-2">
           <div class="card border-secondary">
""" + 'meet.call("127.0.0.1", "/ad", [])' + """
           </div>
        </div>
      </div>
    </div>
    <script type="text/javascript" src="/static/js/bootstrap.bundle.min.js"></script>
  </body>
  </html>"""

@meet.route('/')
def main():
    return make_page("""
<div class="list-group list-group-flush">
<a class="list-group-item list-group-item-action" href="/2/profile">Your profile</a>
<a class="list-group-item list-group-item-action" href="/2/users">Users</a>
<a class="list-group-item list-group-item-action" href="/2/categories">Categories</a>
<a class="list-group-item list-group-item-action" href="/2/events">Events</a>
<a class="list-group-item list-group-item-action" href="/2/locations">Locations</a>
<a class="list-group-item list-group-item-action list-group-item-dark" href="/">Back to the Databank</a>
</div>
""")

def location_html(location):
    location_ = meet.sql("SELECT * FROM locations WHERE id = ?0", [location])[0]
    if location_ == None:
        return ""
    else:
        return location_[2] + " (" + location_[1] + ")"

def error_html(msg):
    return """<div class="alert alert-danger" role="alert">""" + msg + """</div>"""

def location_select(selected):
    options = "<option value=\"0\"></option>"
    locations = meet.sql("SELECT locations.* FROM locations INNER JOIN friends ON locations.owner = friends.friend_id WHERE friends.user_id = ?0 OR locations.owner = ?0", [meet.me()])
    L = len(locations)
    i = 0
    while i < L:
        location = locations[i]
        if selected == location[0]:
            sel = " selected=\"selected\""
        else:
            sel = ""
        options += "<option value=\"" + str(location[0]) + "\"" + sel + ">" + location[2] + " (" + location[1] + ")</option>"
        i = i + 1
    return "<select name=\"location\" id=\"location\" class=\"form-select\">" + options + "</select>"
    
def event_html(event, details):
    title = event[1]
    description = event[2]
    if event[3] > 0:
        location = location_html(event[3])
    else:
        location =  ""
    time_date = event[4] + " " + event[5]
    if details:
        attended = len(meet.sql("SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1", [event[0], meet.me()]))
        if attended > 0:
            leave = "<tr><td colspan\"2\"><a href=\"/2/leave_event/" + str(event[0]) + "\">Leave</a></td></tr>"
        else:
            leave = "<tr><td colspan\"2\"><a href=\"/2/request_attendance/" + str(event[0]) + "\">Request attendance</a></td></tr>"
        invitations = meet.sql("SELECT * FROM invitations WHERE invitee = ?0 AND event = ?1", [meet.me(), event[0]])
        if len(invitations) > 0:
            invitation = invitations[0][0]
            leave += "<tr><td colspan\"2\"><a href=\"/2/accept_invitation/" + str(invitation) + "\">Accept</a>&nbsp;<a href=\"/2/reject_invitation/" + str(invitation) + "\">Reject</a></td></tr>"
    else:
        leave = ""
    leave += "<tr><td colspan\"2\"><a href=\"/2/event/" + str(event[0]) + "\">Details</a></td></tr>"
    return '<table class="table"><thead><tr><th colspan="2">' + title + "</th></tr></thead><tbody><tr><td>Description</td><td>" + description + "</td></tr><tr><td>Location</td><td>" + location + "</td></tr><tr><td>Time/date</td><td>" + time_date + "</td></tr>" + leave + "</tbody></table>"

def is_admin():
    level = meet.sql("SELECT level FROM users WHERE user_id = ?0", [meet.me()])[0][0]
    return level == 3

def is_premium():
    level = meet.sql("SELECT level FROM users WHERE user_id = ?0", [meet.me()])[0][0]
    return level >= 2

def is_registered():
    return len(meet.sql("SELECT * FROM users WHERE user_id = ?0", [meet.me()])) > 0

def is_moderator(ev):
    return len(meet.sql("SELECT cat_mod.* FROM cat_mod JOIN ev_cat ON ev_cat.category = cat_mod.category WHERE cat_mod.moderator = ?0 AND ev_cat.event = ?1", [meet.me(), ev])) > 0

def is_manager(ev):
    return (len(meet.sql("SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1 AND level = 2",
                          [ev, meet.me()])) > 0) \
           or (meet.sql("SELECT owner FROM events WHERE id = ?0", [ev])[0][0] == meet.me())

def is_attendee(ev):
    return (len(meet.sql("SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1",
                          [ev, meet.me()])) > 0) \
           or (meet.sql("SELECT owner FROM events WHERE id = ?0", [ev])[0][0] == meet.me())

@meet.route('/profile')
def profile():
    html = ''
    header = '<h5 class="card-header">Profile</h5>'
    if is_registered():
        owned_events_html = '<div class="card-header">My events</div><div class="card-body"><div class="card-text">'
        owned_events = meet.sql("SELECT * FROM events WHERE owner = ?0", [meet.me()])
        L = len(owned_events)
        i = 0
        while i < L:
            owned_event = owned_events[i]
            owned_events_html += "<br>" + event_html(owned_event, False)
            i = i + 1
        managed_events_html = '</div></div><div class="card-header">Managed events</div><div class="card-body"><div class="card-text">'
        managed_events = meet.sql("SELECT events.* FROM events JOIN ev_att ON events.id = ev_att.event WHERE ev_att.attendee = ?0 AND ev_att.level = 2", [meet.me()])
        L = len(managed_events)
        i = 0
        while i < L:
            managed_event = managed_events[i]
            managed_events_html += "<br>" + event_html(managed_event, False)
            i = i + 1
        attended_events_html = '</div></div><div class="card-header">Attended events</div><div class="card-body"><div class="card-text">'
        attended_events = meet.sql("SELECT events.* FROM events JOIN ev_att ON events.id = ev_att.event WHERE ev_att.attendee = ?0 AND ev_att.level = 1", [meet.me()])
        L = len(attended_events)
        i = 0
        while i < L:
            attended_event = attended_events[i]
            attended_events_html += "<br>" + event_html(attended_event, False)
            i = i + 1
        invited_events_html = '</div></div><div class="card-header">Pending invitations</div><div class="card-body"><div class="card-text">'
        invited_events = meet.sql("SELECT events.* FROM events JOIN invitations ON events.id = invitations.event WHERE invitations.invitee = ?0", [meet.me()])
        L = len(invited_events)
        i = 0
        while i < L:
            inviter = meet.sql("SELECT name FROM users WHERE user_id = ?0", [invited_events[i][6]])[0][0]
            ev      = invited_events[i]
            invited_events_html += "<br><strong>" + inviter + "</strong> invited you to " + event_html(ev, True)
            i = i + 1
        unregister_html = '</div></div><div class="card-header">Unregister</div><div class="card-body"><div class="card-text"><a href="/2/unregister">Unregister</a>'
        footer = '</div></div>'
        html = header + owned_events_html + managed_events_html + attended_events_html + invited_events_html + unregister_html + footer
    else:
        register_html = """<div class="card-header">Register</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/register">
      <input type="hidden" name="ID" id="ID" value=\"""" + str(meet.me()) + """">
      <div class="form-group mb-1">
        <label for="name" class="form-label">Name</label>
        <input type="text" name="name" id="name" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="location" class="form-label">Address</label>
        """ + location_select(0) + """
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
  </div>
</div>"""
        html = header + register_html
    return make_page(html)

@meet.route('/leave_event/<int:ev>')
def leave_event(ev):
    meet.sql("DELETE FROM ev_att WHERE attendee = ?0 AND event = ?1 AND level = 1",
               [meet.me(), ev])
    return profile()

@meet.route('/request_attendance/<int:ev>')
def request_attendance(ev):
    meet.sql("INSERT INTO requests (requester, event) VALUES (?0, ?1)",
               [meet.me(), ev])
    return events()

@meet.route('/reject_invitation/<int:invitation>')
def reject_invitation(invitation):
    meet.sql("DELETE FROM invitations WHERE invitee = ?0 AND id = ?1", [meet.me(), invitation])
    return profile()

@meet.route('/accept_invitation/<int:invitation>')
def accept_invitation(invitation):
    event_id = meet.sql("SELECT event FROM invitations WHERE invitee = ?0 AND id = ?1",
                          [meet.me(), invitation])
    event_id = event_id[0][0]
    meet.sql("INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)", [event_id, meet.me()])
    meet.sql("DELETE FROM invitations WHERE invitee = ?0 AND id = ?1", [meet.me(), invitation])
    return profile()

@meet.route('/unregister')
def unregister():
    meet.sql("DELETE FROM users WHERE user_id = ?0", [meet.me()])
    meet.sql("DELETE FROM cat_mod WHERE moderator = ?0", [meet.me()])
    meet.sql("DELETE FROM cat_sub WHERE subscriber = ?0", [meet.me()])
    meet.sql("DELETE FROM ev_att WHERE attendee = ?0", [meet.me()])
    meet.sql("DELETE FROM events WHERE owner = ?0", [meet.me()])
    meet.sql("DELETE FROM friends WHERE user_id = ?0 OR friend_id = ?0", [meet.me()])
    meet.sql("DELETE FROM invitations WHERE inviter = ?0 OR invitee = ?0", [meet.me()])
    meet.sql("DELETE FROM locations WHERE owner = ?0", [meet.me()])
    meet.sql("DELETE FROM requests WHERE requester = ?0", [meet.me()])
    return profile()

@meet.route('/register')
def register():
    if not is_registered():
        ID      = meet.me()
        name    = meet.get('name')
        level   = 1
        address = int(meet.get('location'))
        meet.sql("INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)",
                   [ID, name, level, address])
    return profile()

@meet.route('/users')
def users():
    header = """<h5 class="card-header">Users</h5>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr>
          <th>ID</th><th>Name</th><th>Level</th><th>Address</th><th>Actions</th>
        </tr>
      </thead>
      <tbody>
"""
    table  = ""
    footer = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Add friend</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/add_friend">
      <div class="form-group mb-1">
        <label for="ID" class="form-label">ID</label>
        <input type="number" step=1 name="ID" id="ID" class="form-control">
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
  </div>
</div>
"""
    if is_registered():
        friends = meet.sql("SELECT users.* FROM friends LEFT JOIN users ON friends.friend_id = users.user_id WHERE friends.user_id = ?0 OR users.user_id = ?0", [meet.me()])
        L = len(friends)
        i = 0
        while i < L:
            user = friends[i]
            table += "<tr><td>" + str(user[1]) + "</td><td>" + user[2] + "</td><td>"
            if user[3] == 1:
                table += "free"
            elif user[3] == 2:
                table += "premium"
            elif user[3] == 3:
                table += "administrator"
            if user[4] > 0:
                table += "</td><td>" + location_html(user[4]) + "</td>"
            else:
                table += "</td><td></td>"
            if user[1] == meet.me():
                table += "<td><a href=\"/2/update_user/" + str(user[1]) + "\">Update</a>&nbsp;<a href=\"/2/user_categories/" + str(user[1]) + "\">Categories</a></td></tr>"
            elif is_admin():
                table += "<td><a href=\"/2/delete_friend/" + str(user[1]) + "\">Delete friend</a>&nbsp;<a href=\"/2/update_user/" + str(user[1]) + "\">Update</a>&nbsp;<a href=\"/2/user_categories/" + str(user[1]) + "\">Categories</a></td></tr>"
            else:
                table += "<td><a href=\"/2/delete_friend/" + str(user[1]) + "\">Delete friend</a>&nbsp;<a href=\"/2/user_categories/" + str(user[1]) + "\">Categories</a></td></tr>"
            i = i + 1
        return make_page(header + table + footer)
    else:
        return make_page("""<h5 class="card-header">Users</h5>
<div class="card-body">
  <div class="card-text">
    Not available for non-registered users
  </div>
</div>""")

@meet.route('/delete_friend/<int:user>')
def delete_friend(user):
    meet.sql("DELETE FROM friends WHERE user_id = ?0 AND friend_id = ?1", [meet.me(), user])
    return users()

@meet.route('/add_friend')
def add_friend():
    user_id   = meet.me()
    friend_id = int(meet.get('ID'))
    if len(meet.sql("SELECT * FROM friends WHERE user_id = ?0 AND friend_id = ?1", [user_id, friend_id])) == 0:
        if len(meet.sql("SELECT * FROM users WHERE user_id = ?0", [friend_id])) > 0:
            meet.sql("INSERT INTO friends (user_id, friend_id) VALUES (?0, ?1)", [user_id, friend_id])
        else:
            return error_html('User ' + str(friend_id) + ' is not registered.<br>\n') + users()
    return users()

@meet.route('/update_user/<int:user>')
def update_user(user):
    user = meet.sql("SELECT * FROM users WHERE user_id = ?0", [user])[0]
    id_     = str(user[0])
    ID      = str(user[1])
    name    = user[2]
    if user[3] == 1:
        free = " selected"
    else:
        free = ""
    if user[3] == 2:
        premium = " selected"
    else:
        premium = ""
    if user[3] == 3:
        administrator = " selected"
    else:
        administrator = ""
    address = user[4]
    return make_page("""<h5 class="card-header">Update user</h5>
<div class="card-body">
  <div class="card-text">
     <form action="/2/update_user_do">
       <input type="hidden" name="id_" id="id_" value=\"""" + id_ + """\">
       <div class="form-group mb-1">
         <label for="ID" class="form-label">ID</label>
         <input type="number" step=1 name="ID" id="ID" value=\"""" + ID + """\" class="form-control">
       </div>
       <div class="form-group mb-1">
         <label for="name" class="form-label">Name</label>
         <input type="text" name="name" id="name" value=\"""" + name + """\" class="form-control">
       </div>
       <div class="form-group mb-1">
         <label for="level" class="form-label">Level</label>
         <select name="level" class="form-select">
           <option value=1""" + free + """>Free</option>
           <option value=2""" + premium + """>Premium</option>
           <option value=3""" + administrator + """>Administrator</option>
         </select>
       </div>
       <div class="form-group mb-1">
         <label for="location" class="form-label">Location</label>
         """ + location_select(address) + """
       </div>
       <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/users">Back to users</a>
</div>
""")

@meet.route('/update_user_do')
def update_user_do():
    id_     = int(meet.get('id_'))
    ID      = int(meet.get('ID'))
    name    = meet.get('name')
    level   = int(meet.get('level'))
    address = int(meet.get('location'))
    if is_admin() or id_ == meet.me():
        meet.sql("DELETE FROM users WHERE id = ?0", [id_])
        meet.sql("INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)",
                   [ID, name, level, address])
        return users()
    else:
        return error_html("Illegal operation: Update user") + users()

@meet.route('/user_categories/<int:user>')
def user_categories(user):
    usr = meet.sql("SELECT * FROM users WHERE user_id = ?0", [user])[0]
    header = """<h5 class="card-header">Categories of user """ + usr[2] + """</h5>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>Category</th><th>Events</th><th>Actions</th></tr>
      </thead>
      <tbody>"""
    categories_html = ""
    footer = """
      </tbody>
    </table>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/users">Back to users</a>
</div>"""
    categories = meet.sql("SELECT * FROM categories")
    L = len(categories)
    i = 0
    while i < L:
        category = categories[i]
        categories_html += "<tr><td>" + category[1] + "</td><td>"
        if len(meet.sql("SELECT id FROM cat_sub WHERE category = ?0 AND subscriber = ?1",
                          [category[0], user])) > 0:
            events = meet.sql("SELECT events.* FROM events JOIN ev_cat ON ev_cat.event = events.id WHERE ev_cat.category = ?0", [category[0]])
            M = len(events)
            j = 0
            while j < M:
                ev = events[j]
                categories_html += event_html(ev, True) + "<br>"
                j = j + 1
            if is_admin() or user == meet.me():
                categories_html += "</td><td><a href=\"/2/unsubscribe/" + str(category[0]) + "/" + str(user) + "\">Unsubscribe</a></td></tr>"
            else:
                categories_html += "</td><td></td></tr>"
        else:
            if is_admin() or user == meet.me():
                categories_html += "</td><td><a href=\"/2/subscribe/" + str(category[0]) + "/" + str(user) + "\">Subscribe</a></td></tr>"
            else:
                categories_html += "</td><td></td></tr>"
        i = i + 1
    return make_page(header + categories_html + footer)

@meet.route('/unsubscribe/<int:category>/<int:user>')
def unsubscribe(category, user):
    if is_admin() or user == meet.me():
        meet.sql("DELETE FROM cat_sub WHERE category = ?0 AND subscriber = ?1", [category, user])
        return user_categories(user)
    else:
        return error_html("Illegal operation: Unsubscribe") + user_categories(user)

@meet.route('/subscribe/<int:category>/<int:user>')
def subscribe(category, user):
    if is_admin() or user == meet.me():
        level = meet.sql("SELECT level FROM users WHERE user_id = ?0", [user])[0][0]
        if level == 1:
            subscriptions = meet.sql("SELECT * FROM cat_sub WHERE subscriber = ?0", [user])
            if len(subscriptions) > 2:
                return "Illegal operation: Subscribe<br>\n" + user_categories(user)
        meet.sql("INSERT INTO cat_sub (category, subscriber) VALUES (?0, ?1)", [category, user])
        return user_categories(user)
    else:
        return error_html("Illegal operation: Subscribe") + user_categories(user)

@meet.route('/categories')
def categories():
    header = """<h5 class="card-header">Categories</h5>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
    table  = ""
    if is_admin():
        footer = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Add new category</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/add_category">
      <div class="form-group mb-1">
        <label for="name" class="form-label">Name</label>
        <input type="text" name="name" id="name" class="form-control">
      </div>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
"""
    else:
        footer = """
      </tbody>
    </table>
  </div>
</div>"""
    categories = meet.sql("SELECT categories.* FROM friends LEFT JOIN categories ON categories.owner = friends.friend_id WHERE friends.user_id = ?0 OR categories.owner = ?0", [meet.me()])
    L = len(categories)
    i = 0
    while i < L:
        cat = categories[i]
        if is_admin():
            table += "<tr><td>" + str(cat[1]) + "</td><td><a href=\"/2/delete_category/" + str(cat[0]) + "\">Delete</a>&nbsp;<a href=\"/2/update_category/" + str(cat[0]) + "\">Update</a>&nbsp;<a href=\"/2/category/" + str(cat[0]) + "\">Details</a></td></tr>"
        else:
            table += "<tr><td>" + str(cat[1]) + "</td><td></td></tr>"
        i = i + 1
    return make_page(header + table + footer)

@meet.route('/delete_category/<int:cat>')
def delete_category(cat):
    if is_admin():
        meet.sql("DELETE FROM categories WHERE id = ?0", [cat])
        meet.sql("DELETE FROM cat_mod WHERE category = ?0", [cat])
        meet.sql("DELETE FROM cat_sub WHERE category = ?0", [cat])
        meet.sql("DELETE FROM ev_cat WHERE category = ?0", [cat])
        return categories()
    else:
        return error_html("Illegal operation: Delete category") + categories()

@meet.route('/add_category')
def add_category():
    if is_admin():
        name    = meet.get('name')
        meet.sql("INSERT INTO categories (name, owner) VALUES (?0, ?1)", [name, meet.me()])
        return categories()
    else:
        return error_html("Illegal operation: Add category") + categories()

@meet.route('/update_category/<int:cat>')
def update_category(cat):
    cat_    = meet.sql("SELECT * FROM categories WHERE id = ?0", [cat])[0]
    id_     = str(cat_[0])
    name    = cat_[1]
    return make_page("""<h5 class="card-header">Update category</h5>
<div class="card-body">
  <div class="card-text">
    <form action="/2/update_category_do">
      <input type="hidden" name="id_" id="id_" value=\"""" + id_ + """\">
      <div class="form-group mb-1">
        <label for="name" class="form-label">Name</label>
        <input type="text" name="name" id="name" value=\"""" + name + """\" class="form-control">
      </div>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/categories">Back to categories</a>
</div>
""")

@meet.route('/update_category_do')
def update_category_do():
    if not is_admin():
        return error_html("Illegal operation: Update category") + categories()
    id_     = int(meet.get('id_'))
    name    = meet.get('name')
    owner   = meet.sql("SELECT owner FROM categories WHERE id = ?0", [id_])[0][0]
    meet.sql("DELETE FROM categories WHERE id = ?0", [id_])
    new_id  = meet.sql("INSERT INTO categories (name, owner) VALUES (?0, ?1)", [name, owner])[0]
    # update bindings cat_mods
    cat_mods = meet.sql("SELECT * FROM cat_mod WHERE category = ?0", [id_])
    L = len(cat_mods)
    i = 0
    while i < L:
        cat_mod = cat_mods[i]
        meet.sql("DELETE FROM cat_mod WHERE id = ?0", [cat_mod[0]])
        meet.sql("INSERT INTO cat_mod (category, moderator) VALUES (?0, ?1)", [new_id, cat_mod[2]])
        i = i + 1
    # update bindings cat_sub
    cat_subs = meet.sql("SELECT * FROM cat_sub WHERE category = ?0", [id_])
    L = len(cat_subs)
    i = 0
    while i < L:
        cat_sub = cat_subs[i]
        meet.sql("DELETE FROM cat_sub WHERE id = ?0", [cat_sub[0]])
        meet.sql("INSERT INTO cat_sub (category, subscriber) VALUES (?0, ?1)", [new_id, cat_sub[2]])
        i = i + 1
    # update bindings ev_cat
    ev_cats = meet.sql("SELECT * FROM ev_cat WHERE category = ?0", [id_])
    L = len(ev_cats)
    i = 0
    while i < L:
        ev_cat = ev_cats[i]
        meet.sql("DELETE FROM ev_cat WHERE id = ?0", [ev_cat[0]])
        meet.sql("INSERT INTO ev_cat (event, category) VALUES (?0, ?1)", [ev_cat[1], new_id])
        i = i + 1
    return categories()

@meet.route('/category/<int:cat>')
def category(cat):
    name = meet.sql("SELECT name FROM categories WHERE id = ?0", [cat])[0][0]
    header = '<h5 class="card-header">Category ' + name + "</h5>"
    is_subscriber = len(meet.sql("SELECT * FROM cat_sub WHERE category = ?0 AND subscriber = ?1",
                                   [cat, meet.me()])) > 0
    moderators_html = ""
    subscribers_html = ""
    if is_subscriber:
        moderators_html = """<div class="card-header">Moderators</div>"""
        if is_admin() or is_moderator(cat):
            moderators_html += """
<div class="card-body">
  <a href="/2/category_moderators/""" + str(cat) + """">Modify</a>
</div>"""
        moderators_html += """
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th></tr>
      </thead>
      <tbody>
"""
        moderators = meet.sql("SELECT users.* FROM users JOIN cat_mod ON cat_mod.moderator = users.id WHERE cat_mod.category = ?0", [cat])
        L = len(moderators)
        i = 0
        while i < L:
            moderator = moderators[i]
            moderators_html += "<tr><td>" + str(moderator[1]) + "</td><td>" + moderator[2] + "</td></tr>"
            i = i + 1
        subscribers_html = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Subscribers</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th></tr>
      </thead>
      <tbody>
"""
        subscribers = meet.sql("SELECT users.* FROM users JOIN cat_sub ON cat_sub.subscriber = users.id WHERE cat_sub.category = ?0", [cat])
        L = len(subscribers)
        i = 0
        while i < L:
            subscriber = subscribers[i]
            subscribers_html += "<tr><td>" + str(subscriber[1]) + "</td><td>" + subscriber[2] + "</td></tr>"
            i = i + 1
        events_html = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Events</div>
<div class="card-body">
  <div class="card-text">
"""
    else:
        events_html = """
<div class="card-header">Events</div>
<div class="card-body">
  <div class="card-text">
"""    
    events = meet.sql("SELECT events.* FROM events JOIN ev_cat ON ev_cat.event = events.id WHERE ev_cat.category = ?0", [cat])
    L = len(events)
    i = 0
    while i < L:
        events_html += event_html(events[i], True)
        i = i + 1
    footer = """
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/categories">Back to categories</a>
</div>"""
    return make_page(header + moderators_html + subscribers_html + events_html + footer)

@meet.route('/category_moderators/<int:cat>')
def category_moderators(cat):
    if is_admin():
        name = meet.sql("SELECT name FROM categories WHERE id = ?0", [cat])[0][0]
        header = """<h5 class="card-header">Moderators of category """ + name + """</h5>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
        current_html = ""
        footer1 = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Add new moderators</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
        new_html = ""
        footer2 = """
      </tbody>
    </table>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/category/""" + str(cat) + """">Back to category</a>
</div>"""
        users = meet.sql("SELECT id, user_id, name FROM users", [cat])
        L = len(users)
        i = 0
        while i < L:
            user = users[i]
            if len(meet.sql("SELECT * FROM cat_mod WHERE category = ?0 AND moderator = ?1", [cat, user[0]])) > 0:
                current_html += "<tr><td>" + str(user[1]) + "</td><td>" + user[2] + "</td><td><a href=\"/2/delete_category_moderator/" + str(cat) + "/" + str(user[0]) + "\">Remove moderator</a></td></tr>"
            else:
                new_html += "<tr><td>" + str(user[1]) + "</td><td>" + user[2] + "</td><td><a href=\"/2/add_category_moderator/" + str(cat) + "/" + str(user[0]) + "\">Make moderator</a></td></tr>"
            i = i + 1
        return make_page(header + current_html + footer1 + new_html + footer2)
    else:
        return error_html("Illegal operation: Category moderators") + category(cat)
        
@meet.route('/delete_category_moderator/<int:cat>/<int:user>')
def delete_category_moderator(cat, user):
    if is_admin():
        meet.sql("DELETE FROM cat_mod WHERE category = ?0 AND moderator = ?1", [cat, user])
        return category_moderators(cat)
    else:
        return error_html("Illegal operation: Delete category moderator") + category(cat)

@meet.route('/add_category_moderator/<int:cat>/<int:user>')
def add_category_moderator(cat, user):
    if is_admin():
        meet.sql("INSERT INTO cat_mod (category, moderator) VALUES (?0, ?1)", [cat, user])
        return category_moderators(cat)
    else:
        return error_html("Illegal operation: Add category moderator") + category(cat)

@meet.route('/events')
def events():
    return events_from(0)

@meet.route('/events/<int:start>')
def events_from(start):
    header      = """<h5 class="card-header">Events</h5>
<div class="card-body">
  <div class="card-text">
"""
    events_html = ""
    footer      = """
  </div>
</div>
<div class="card-header">Add new event</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/add_event">
      <div class="form-group mb-1">
        <label for="title" class="form-label">Title</label>
        <input type="text" name="title" id="title" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="description" class="form-label">Description</label>
        <input type="text" name="description" id="description" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="location" class="form-label">Location</label>
        """ + location_select(0) + """
      </div>
      <div class="form-group mb-1">
        <label for="time" class="form-label">Time</label>
        <input type="text" name="time" id="time" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="date" class="form-label">Date</label>
        <input type="text" name="date" id="date" class="form-control">
      </div>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
"""
    events = meet.sql("SELECT events.* FROM events LEFT JOIN friends ON events.owner = friends.friend_id WHERE friends.user_id = ?0 OR events.owner = ?0 ORDER BY events.id DESC LIMIT 5 OFFSET ?1", [meet.me(), start])
    L = len(meet.sql("SELECT events.id FROM events LEFT JOIN friends ON events.owner = friends.friend_id WHERE friends.user_id = ?0 OR events.owner = ?0 LIMIT 6 OFFSET ?1", [meet.me(), start]))
    L2 = len(events)
    i = 0
    while i < L2:
        ev = events[i]
        events_html += event_html(ev, True) + "<br>"
        i = i + 1
    if (start > 0) or (L > 5):
        events_html = """  </ul>
</nav>""" + events_html
        if L > 5:
            events_html = """<li class="page-item"><a class="page-link" href=\"/2/events/""" + str(start+5) + "\">Events " + str(start+6) + "-...</a></li>" + events_html
        events_html = """<li class="page-item active"><a class="page-link" href="#">Events """ + str(start+1) + "-" + str(start+5) + "</a></li>""" + events_html
        if start > 0:
            events_html = """<li class="page-item"><a class="page-link" href="/2/events/""" + str(start-5) + "\">Events " + str(start-4) + "-" + str(start) + "</a></li>" + events_html
        events_html = """<nav>
  <ul class="pagination">""" + events_html
    return make_page(header + events_html + footer)

@meet.route('/add_event')
def add_event():
    title       = meet.get('title')
    description = meet.get('description')
    location    = int(meet.get('location'))
    time        = meet.get('time')
    date        = meet.get('date')
    owner       = meet.me()
    level = meet.sql("SELECT level FROM users WHERE user_id = ?0", [meet.me()])[0][0]
    owned = len(meet.sql("SELECT * FROM events WHERE owner = ?0 LIMIT 3", [meet.me()]))
    if level == 1 and owned > 2:
        return error_html("Illegal operation: Add event") + events()
    else:
        meet.sql("INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)",
                   [title, description, location, time, date, owner])
        return events()

@meet.route('/event/<int:ev>')
def event(ev):
    evt = meet.sql("SELECT * FROM events WHERE id = ?0", [ev])[0]
    html = """<h5 class="card-header">Event</h5>
<div class="card-body">
  <div class="card-text">
    """ + event_html(evt, True) + """
  </div>
</div>
<div class="card-header">Managers</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
    managers = meet.sql("SELECT users.user_id, users.name FROM users JOIN ev_att ON ev_att.attendee = users.user_id WHERE ev_att.event = ?0 AND ev_att.level = 2", [ev])
    L = len(managers)
    i = 0
    while i < L:
        manager = managers[i]
        html += "<tr><td>" + str(manager[0]) + "</td><td>" + manager[1] + "</td>"
        if evt[6] == meet.me() and is_premium():
            html += "<td><a href=\"/2/revoke_moderator/" + str(ev) + "/" + str(manager[0]) + "\">Revoke</a></td></tr>"
        else:
            html += "<td></td></tr>"
        i = i + 1
    if is_attendee(ev) or (is_manager(ev) or is_premium()):
        html = html + """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Attendees</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
        attendees = meet.sql("SELECT users.user_id, users.name FROM users JOIN ev_att ON ev_att.attendee = users.user_id WHERE ev_att.event = ?0 AND ev_att.level = 1", [ev])
        L = len(attendees)
        i = 0
        while i < L:
            attendee = attendees[i]
            html += "<tr><td>" + str(attendee[0]) + "</td><td>" + attendee[1] + "</td>"
            if is_manager(ev) or (evt[6] == meet.me() and is_premium()):
                html += "<td><a href=\"/2/promote_attendee/" + str(ev) + "/" + str(attendee[0]) + "\">Promote to manager</a></td></tr>"
            else:
                html += "<td></td></tr>"
            i = i + 1
    if is_manager(ev):
        html += """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Attendance requests</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
        requesters = meet.sql("SELECT users.user_id, users.name FROM users JOIN requests ON requests.requester = users.user_id WHERE requests.event = ?0", [ev])
        L = len(requesters)
        i = 0
        while i < L:
            requester = requesters[i]
            html += "<tr><td>" + str(requester[0]) + "</td><td>" + str(requester[1]) + "</td><td><a href=\"/2/accept_request/" + str(ev) + "/" + str(requester[0]) + "\">Accept</a>&nbsp;<a href=\"/2/reject_request/" + str(ev) + "/" + str(requester[0]) + "\">Reject</a>&nbsp;</td></tr>"
            i = i + 1
        html += """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Categories</div>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
        cats = meet.sql("SELECT categories.* FROM categories LEFT JOIN friends ON friends.friend_id = categories.owner WHERE friends.user_id = ?0 OR categories.owner = ?0", [meet.me()])
        L = len(cats)
        i = 0
        while i < L:
            cat = cats[i]
            is_event_category = len(meet.sql("SELECT * FROM ev_cat WHERE event = ?0 AND category = ?1",
                                                   [ev, cat[0]])) > 0
            
            if is_event_category:
                html += "<tr><td>" + str(cat[1]) + " (selected)</td><td><a href=\"/2/delete_event_category/" + str(ev) + "/" + str(cat[0]) + "\">Delete</td></tr>"
            else:
                html += "<tr><td>" + str(cat[1]) + "</td><td><a href=\"/2/add_event_category/" + str(ev) + "/" + str(cat[0]) + "\">Add</td></tr>"
            i += 1
        html += """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Actions</div>
<div class="card-body">
  <div class="card-text">
    <a href=\"/2/update_event/""" + str(ev) + """">Update</a>&nbsp;<a href="/2/delete_event/""" + str(ev) + """">Delete</a><br>
"""
        html += """
  </div>
</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/invite/""" + str(ev) + """" class="row">
      <div class="col-auto">
        <input type="text" readonly class="form-control-plaintext" value="Invite user with ID">
      </div>
      <div class="col-auto">
        <input type="number" step=1 name="ID" id="ID" class="form-control">
      </div>
      <div class="col-auto">
        <input type="submit" value="Submit" class="btn btn-primary">
      </div>
    </form>
  </div>
</div>
"""
    if is_moderator(ev):
        html += """
<div class="card-header">Actions</div>
<div class="card-body">
  <div class="card-text">
    <a href=\"/2/update_event/""" + str(ev) + """">Update</a>
  </div>
</div>"""
    html += """
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/events">Back to events</a>
</div>"""
    return make_page(html)

@meet.route('/add_event_category/<int:ev>/<int:cat>')
def add_event_category(ev, cat):
    if is_manager(ev):
        meet.sql("INSERT INTO ev_cat (event, category) VALUES (?0, ?1)", [ev, cat])
        return event(ev)
    else:
        return error_html("Illegal operation: Add event category") + event(ev)

@meet.route('/delete_event_category/<int:ev>/<int:cat>')
def delete_event_category(ev, cat):
    if is_manager(ev):
        meet.sql("DELETE FROM ev_cat WHERE event = ?0 AND category = ?1", [ev, cat])
        return event(ev)
    else:
        return error_html("Illegal operation: Delete event category") + event(ev)

@meet.route('/delete_event/<int:ev>')
def delete_event(ev):
    if is_manager(ev):
        meet.sql("DELETE FROM events WHERE id = ?0", [ev])
        meet.sql("DELETE FROM ev_att WHERE event = ?0", [ev])
        meet.sql("DELETE FROM ev_cat WHERE event = ?0", [ev])
        meet.sql("DELETE FROM invitations WHERE event = ?0", [ev])
        meet.sql("DELETE FROM requests WHERE event = ?0", [ev])
        return events()
    else:
        return error_html("Illegal operation: Delete event") + events()

@meet.route('/update_event/<int:ev>')
def update_event(ev):
    evt = meet.sql("SELECT * FROM events WHERE id = ?0", [ev])[0]
    title        = evt[1]
    description  = evt[2]
    if evt[3] > 0:
        location = location_html(evt[3])
    else:
        location = ""
    time         = evt[4]
    date         = evt[5]
    owner        = str(evt[6])
    return make_page("""<h5 class="card-header">Update event</h5>
<div class="card-body">
  <div class="card-text">
    <form action="/2/update_event_do">
      <div class="form-group mb-1">
        <label for="title" class="form-label">Title</label>
        <input type="text" name="title" id="title" value=\"""" + title + """" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="description" class="form-label">Description</label>
        <input type="text" name="description" id="description" value=\"""" + description + """" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="location" class="form-label">Location</label>
        """ + location_select(evt[3]) + """
      </div>
      <div class="form-group mb-1">
        <label for="time" class="form-label">Time</label>
        <input type="text" name="time" id="time" value=\"""" + time + """" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="time" class="form-label">Date</label>
        <input type="text" name="date" id="date" value=\"""" + date + """" class="form-control">
      </div>
      <input type="hidden" name="owner" id="owner" value=""" + owner + """>
      <input type="hidden" name="id_" id="id_" value=""" + str(ev) + """>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/event/""" + str(ev) + """">Back to event</a>
</div>""")

@meet.route('/update_event_do')
def update_event_do():
    id_ = int(meet.get('id_'))
    if not (is_manager(id_) or is_moderator(id_)):
        return error_html("Illegal operation: Update event") + event(id_)
    else:
        title       = meet.get('title')
        description = meet.get('description')
        location    = int(meet.get('location'))
        time        = meet.get('time')
        date        = meet.get('date')
        owner       = int(meet.get('owner'))
        meet.sql("DELETE FROM events WHERE id = ?0", [id_])
        new_id = meet.sql("INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)",
                            [title, description, location, time, date, owner])[0]
        # update bindings ev_att
        ev_atts = meet.sql("SELECT * FROM ev_att WHERE event = ?0", [id_])
        L = len(ev_atts)
        i = 0
        while i < L:
            ev_att = ev_atts[i]
            meet.sql("DELETE FROM ev_att WHERE id = ?0", [ev_att[0]])
            meet.sql("INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, ?2)",
                       [new_id, ev_att[2], ev_att[3]])
            i = i + 1
        # update bindings ev_cat
        ev_cats = meet.sql("SELECT * FROM ev_cat WHERE event = ?0", [id_])
        L = len(ev_cats)
        i = 0
        while i < L:
            ev_cat = ev_cats[i]
            meet.sql("DELETE FROM ev_cat WHERE id = ?0", [ev_cat[0]])
            meet.sql("INSERT INTO ev_cat (event, category) VALUES (?0, ?1)",
                       [new_id, ev_cat[2]])
            i = i + 1
        # update bindings invitations
        invitations = meet.sql("SELECT * FROM invitations WHERE event = ?0", [id_])
        L = len(invitations)
        i = 0
        while i < L:
            invitation = invitations[i]
            meet.sql("DELETE FROM invitations WHERE id = ?0", [invitation[0]])
            meet.sql("INSERT INTO invitations (inviter, invitee, event) VALUES (?0, ?1, ?2)",
                       [invitation[1], invitation[2], new_id])
            i = i + 1
        # update bindings requests
        requests = meet.sql("SELECT * FROM requests WHERE event = ?0", [id_])
        L = len(requests)
        i = 0
        while i < L:
            request = requests[i]
            meet.sql("DELETE FROM requests WHERE id = ?0", [request[0]])
            meet.sql("INSERT INTO requests (requester, event) VALUES (?0, ?1)",
                       [request[1], new_id])
            i = i + 1
        return event(new_id)

@meet.route('/promote_attendee/<int:ev>/<int:att>')
def promote_attendee(ev, att):
    if is_manager(ev) or (evt[6] == meet.me() and is_premium()):
        meet.sql("DELETE FROM ev_att WHERE event = ?0 AND attendee = ?1", [ev, att])
        meet.sql("INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 2)", [ev, att])
        return event(ev)
    else:
        return error_html("Illegal operation: Promote attendee") + event(ev)

@meet.route('/revoke_moderator/<int:ev>/<int:att>')
def revoke_moderator(ev, att):
    if is_manager(ev) or (evt[6] == meet.me() and is_premium()):
        meet.sql("DELETE FROM ev_att WHERE event = ?0 AND attendee = ?1", [ev, att])
        meet.sql("INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)", [ev, att])
        return event(ev)
    else:
        return error_html("Illegal operation: Revoke moderator") + event(ev)

@meet.route('/accept_request/<int:ev>/<int:req>')
def accept_request(ev, req):
    if is_manager(ev):
        meet.sql("DELETE FROM requests WHERE event = ?0 AND requester = ?1", [ev, req])
        meet.sql("INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)", [ev, req])
        return event(ev)
    else:
        return error_html("Illegal operation: Accept request") + event(ev)

@meet.route('/reject_request/<int:ev>/<int:req>')
def reject_request(ev, req):
    if is_manager(ev):
        meet.sql("DELETE FROM requests WHERE event = ?0 AND requester = ?1", [ev, req])
        return event(ev)
    else:
        return error_html("Illegal operation: Reject request") + event(ev)

@meet.route('/invite/<int:ev>')
def invite(ev):
    if is_manager(ev):
        user_id = meet.get('ID')
        meet.sql("INSERT INTO invitations (inviter, invitee, event) VALUES (?0, ?1, ?2)",
                   [meet.me(), user_id, ev])
        return event(ev)
    else:
        return error_html("Illegal operation: Invite") + event(ev)

@meet.route('/locations')
def locations():
    header = """<h5 class="card-header">Locations</h5>
<div class="card-body">
  <div class="card-text">
    <table class="table">
      <thead>
        <tr><th>Country</th><th>Name</th><th>Actions</th></tr>
      </thead>
      <tbody>
"""
    table  = ""
    if is_admin():
        footer = """
      </tbody>
    </table>
  </div>
</div>
<div class="card-header">Add new location</div>
<div class="card-body">
  <div class="card-text">
    <form action="/2/add_location">
      <div class="form-group mb-1">
        <label for="country" class="form-label">Country</label>
        <input type="text" name="country" id="country" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="name" class="form-label">Name</label>
        <input type="text" name="name" id="name" class="form-control">
      </div>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
"""
    else:
        footer = """
      </tbody>
    </table>
  </div>
</div>"""
    locs = meet.sql("SELECT locations.* FROM friends LEFT JOIN locations ON friends.friend_id = locations.owner WHERE friends.user_id = ?0 OR locations.owner = ?0", [meet.me()])
    L = len(locs)
    i = 0
    while i < L:
        location = locs[i]
        table += "<tr><td>" + str(location[1]) + "</td><td>" + str(location[2]) + "</td>"
        if location[3] == meet.me():
            table += "<td><a href=\"/2/delete_location/" + str(location[0]) + "\">Delete</a>&nbsp;<a href=\"/2/update_location/" + str(location[0]) + "\">Update</a></td></tr>"
        else:
            table += "<td></td></tr>"
        i = i + 1
    return make_page(header + table + footer)

@meet.route('/delete_location/<int:location>')
def delete_location(location):
    owner = meet.sql("SELECT owner FROM locations WHERE id = ?0", [location])[0][0]
    if owner != meet.me():
        return error_html("Illegal operation: Delete location") + locations()
    else:
        meet.sql("DELETE FROM locations WHERE id = ?0", [location])
        # update bindings events
        evs = meet.sql("SELECT * FROM events WHERE location = ?0", [id_])
        L = len(evs)
        i = 0
        while i < L:
            ev = evs[i]
            meet.sql("DELETE FROM events WHERE id = ?0", [ev[0]])
            meet.sql("INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)",
                       [ev[1], ev[2], 0, ev[3], ev[4], ev[5]])
            i = i + 1
        # update bindings users
        usrs = meet.sql("SELECT * FROM users WHERE address = ?0", [id_])
        L = len(usrs)
        i = 0
        while i < L:
            usr = usrs[i]
            meet.sql("DELETE FROM users WHERE id = ?0", [usr[0]])
            meet.sql("INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)",
                       [usr[1], usr[2], usr[3], 0])
            i = i + 1
        return locations()

@meet.route('/add_location')
def add_location():
    country = meet.get('country')
    name    = meet.get('name')
    meet.sql("INSERT INTO locations (country, name, owner) VALUES (?0, ?1, ?2)", [country, name, meet.me()])
    return locations()

@meet.route('/update_location/<int:location>')
def update_location(location):
    location_ = meet.sql("SELECT * FROM locations WHERE id = ?0", [location])[0]
    id_       = str(location_[0])
    country   = location_[1]
    name      = location_[2]
    owner     = location_[3]
    return make_page("""<h5 class="card-header">Update location</h5>
<div class="card-body">
  <div class="card-text">
    <form action="/2/update_location_do">
      <input type="hidden" name="id_" id="id_" value=\"""" + id_ + """">
      <input type="hidden" name="owner" id="owner" value=\"""" + owner + """">
      <div class="form-group mb-1">
        <label for="country" class="form-label">Country</label>
        <input type="text" name="country" id="country" value=\"""" + country + """" class="form-control">
      </div>
      <div class="form-group mb-1">
        <label for="name" class="form-label">Name</label>
        <input type="text" name="name" id="name" value=\"""" + name + """" class="form-control">
      </div>
      <input type="submit" value="Submit" class="btn btn-primary">
    </form>
  </div>
</div>
<div class="list-group list-group-flush">
  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/locations">Back to locations</a>
</div>
""")

@meet.route('/update_location_do')
def update_location_do():
    id_   = int(meet.get('id_'))
    owner = meet.sql("SELECT owner FROM locations WHERE id = ?0", [id_])[0][0]
    if owner != meet.me():
        return error_html("Illegal operation: Update location") + locations()
    else:
        country = meet.get('country')
        name    = meet.get('name')
        meet.sql("DELETE FROM locations WHERE id = ?0", [id_])
        new_id = meet.sql("INSERT INTO locations (country, name) VALUES (?0, ?1)", [country, name])[0]
        # update bindings events
        evs = meet.sql("SELECT * FROM events WHERE location = ?0", [id_])
        L = len(evs)
        i = 0
        while i < L:
            ev = evs[i]
            meet.sql("DELETE FROM events WHERE id = ?0", [ev[0]])
            meet.sql("INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)",
                       [ev[1], ev[2], new_id, ev[3], ev[4], ev[5]])
            i = i + 1
        # update bindings users
        usrs = meet.sql("SELECT * FROM users WHERE address = ?0", [id_])
        L = len(usrs)
        i = 0
        while i < L:
            usr = usrs[i]
            meet.sql("DELETE FROM users WHERE id = ?0", [usr[0]])
            meet.sql("INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)",
                       [usr[1], usr[2], usr[3], new_id])
            i = i + 1
        return locations()
