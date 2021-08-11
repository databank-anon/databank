
from apps import meetup
from databank.imports import *
__stack__ = None

def make_page(html):
    global __stack__
    __r__ = Cell(((((Cell('<!doctype html>\n  <head>\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n    \n    <link rel="stylesheet" href="/static/css/bootstrap.min.css">\n        \n    <title>The Databank</title>\n  </head>\n  <body>\n    <header class="navbar navbar-light" id="navbar">\n      <div class="container-fluid">\n        <a class="navbar-brand" href="/2">\n          Meetup\n        </a>\n      </div>\n    </header>\n    <div class="container">\n      <div class="row">\n        <div class="col-sm-8 offset-sm-2">\n           <div class="card">\n') + html) + Cell('\n           </div>\n        </div>\n        <div class="col-sm-2">\n           <div class="card border-secondary">\n')) + Cell('meetup.call("127.0.0.1", "/ad", [])')) + Cell('\n           </div>\n        </div>\n      </div>\n    </div>\n    <script type="text/javascript" src="/static/js/bootstrap.bundle.min.js"></script>\n  </body>\n  </html>')), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def main():
    global __stack__
    try:
        ___2 = make_page(Cell('\n<div class="list-group list-group-flush">\n<a class="list-group-item list-group-item-action" href="/2/profile">Your profile</a>\n<a class="list-group-item list-group-item-action" href="/2/users">Users</a>\n<a class="list-group-item list-group-item-action" href="/2/categories">Categories</a>\n<a class="list-group-item list-group-item-action" href="/2/events">Events</a>\n<a class="list-group-item list-group-item-action" href="/2/locations">Locations</a>\n<a class="list-group-item list-group-item-action list-group-item-dark" href="/">Back to the Databank</a>\n</div>\n'))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___2, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/')
def _main():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = main()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def location_html(location):
    global __stack__
    if ('location_' not in locals()):
        location_ = Cell(None)
    ___3 = meetup.sql(Cell('SELECT * FROM locations WHERE id = ?0'), Cell([location]))
    location_ = ___3[Cell(0)]
    location_.add_inputs(__stack__.all())
    ___4 = Cell((location_ == Cell(None)))
    if ___4:
        __stack__.push()
        __stack__.add(___4.inputs)
        __r__ = Cell(Cell(''), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___4, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___4.inputs, bot=True)
    if non(___4):
        __stack__.push()
        __stack__.add(___4.inputs)
        __r__ = Cell((((location_[Cell(2)] + Cell(' (')) + location_[Cell(1)]) + Cell(')')), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___4, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___4.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

def error_html(msg):
    global __stack__
    __r__ = Cell(((Cell('<div class="alert alert-danger" role="alert">') + msg) + Cell('</div>')), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def location_select(selected):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('sel' not in locals()):
        sel = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    if ('options' not in locals()):
        options = Cell(None)
    options = Cell('<option value="0"></option>')
    options.add_inputs(__stack__.all())
    ___5 = meetup.me()
    ___6 = meetup.sql(Cell('SELECT locations.* FROM locations INNER JOIN friends ON locations.owner = friends.friend_id WHERE friends.user_id = ?0 OR locations.owner = ?0'), Cell([___5]))
    locations = ___6
    locations.add_inputs(__stack__.all())
    ___7 = db_len(locations)
    L = ___7
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___8 = Cell((i < L))
    while ___8:
        __stack__.push()
        __stack__.add(___8.inputs)
        location = locations[i]
        location.add_inputs(__stack__.all())
        ___9 = Cell((selected == location[Cell(0)]))
        if ___9:
            __stack__.push()
            __stack__.add(___9.inputs)
            sel = Cell(' selected="selected"')
            sel.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___9, adopt=__stack__.all()).inputs, [], [], auto=True)
            sel.add_inputs(__stack__.all())
            sel.add_inputs(___9.inputs)
        if non(___9):
            __stack__.push()
            __stack__.add(___9.inputs)
            sel = Cell('')
            sel.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___9, adopt=__stack__.all()).inputs, [], [], auto=True)
            sel.add_inputs(__stack__.all())
            sel.add_inputs(___9.inputs)
        ___10 = db_str(location[Cell(0)])
        options = (options + ((((((((Cell('<option value="') + ___10) + Cell('"')) + sel) + Cell('>')) + location[Cell(2)]) + Cell(' (')) + location[Cell(1)]) + Cell(')</option>')))
        options.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___8 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___8, adopt=__stack__.all()).inputs, [], [], auto=True)
    i.add_inputs(__stack__.all())
    i.add_inputs(___8.inputs)
    location.add_inputs(__stack__.all())
    location.add_inputs(___8.inputs)
    sel.add_inputs(__stack__.all())
    sel.add_inputs(___8.inputs)
    options.add_inputs(__stack__.all())
    options.add_inputs(___8.inputs)
    __r__ = Cell(((Cell('<select name="location" id="location" class="form-select">') + options) + Cell('</select>')), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def event_html(event, details):
    global __stack__
    if ('time_date' not in locals()):
        time_date = Cell(None)
    if ('attended' not in locals()):
        attended = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    if ('invitation' not in locals()):
        invitation = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('leave' not in locals()):
        leave = Cell(None)
    if ('invitations' not in locals()):
        invitations = Cell(None)
    if ('description' not in locals()):
        description = Cell(None)
    title = event[Cell(1)]
    title.add_inputs(__stack__.all())
    description = event[Cell(2)]
    description.add_inputs(__stack__.all())
    ___11 = Cell((event[Cell(3)] > Cell(0)))
    if ___11:
        __stack__.push()
        __stack__.add(___11.inputs)
        try:
            ___12 = location_html(event[Cell(3)])[0]
        except Stop as __stop__:
            time_date.add_inputs(__stop__.inputs)
            invitations.add_inputs(__stop__.inputs)
            invitation.add_inputs(__stop__.inputs)
            location.add_inputs(__stop__.inputs)
            attended.add_inputs(__stop__.inputs)
            leave.add_inputs(__stop__.inputs)
            raise __stop__
        location = ___12
        location.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___11, adopt=__stack__.all()).inputs, [], [], auto=True)
        location.add_inputs(__stack__.all())
        location.add_inputs(___11.inputs)
    if non(___11):
        __stack__.push()
        __stack__.add(___11.inputs)
        location = Cell('')
        location.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___11, adopt=__stack__.all()).inputs, [], [], auto=True)
        location.add_inputs(__stack__.all())
        location.add_inputs(___11.inputs)
    time_date = ((event[Cell(4)] + Cell(' ')) + event[Cell(5)])
    time_date.add_inputs(__stack__.all())
    ___13 = details
    if ___13:
        __stack__.push()
        __stack__.add(___13.inputs)
        ___14 = meetup.me()
        ___15 = meetup.sql(Cell('SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1'), Cell([event[Cell(0)], ___14]))
        ___16 = db_len(___15)
        attended = ___16
        attended.add_inputs(__stack__.all())
        ___17 = Cell((attended > Cell(0)))
        if ___17:
            __stack__.push()
            __stack__.add(___17.inputs)
            ___18 = db_str(event[Cell(0)])
            leave = ((Cell('<tr><td colspan"2"><a href="/2/leave_event/') + ___18) + Cell('">Leave</a></td></tr>'))
            leave.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___17, adopt=__stack__.all()).inputs, [], [], auto=True)
            leave.add_inputs(__stack__.all())
            leave.add_inputs(___17.inputs)
        if non(___17):
            __stack__.push()
            __stack__.add(___17.inputs)
            ___19 = db_str(event[Cell(0)])
            leave = ((Cell('<tr><td colspan"2"><a href="/2/request_attendance/') + ___19) + Cell('">Request attendance</a></td></tr>'))
            leave.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___17, adopt=__stack__.all()).inputs, [], [], auto=True)
            leave.add_inputs(__stack__.all())
            leave.add_inputs(___17.inputs)
        ___20 = meetup.me()
        ___21 = meetup.sql(Cell('SELECT * FROM invitations WHERE invitee = ?0 AND event = ?1'), Cell([___20, event[Cell(0)]]))
        invitations = ___21
        invitations.add_inputs(__stack__.all())
        ___22 = db_len(invitations)
        ___23 = Cell((___22 > Cell(0)))
        if ___23:
            __stack__.push()
            __stack__.add(___23.inputs)
            invitation = invitations[Cell(0)][Cell(0)]
            invitation.add_inputs(__stack__.all())
            ___24 = db_str(invitation)
            ___25 = db_str(invitation)
            leave = (leave + ((((Cell('<tr><td colspan"2"><a href="/2/accept_invitation/') + ___24) + Cell('">Accept</a>&nbsp;<a href="/2/reject_invitation/')) + ___25) + Cell('">Reject</a></td></tr>')))
            leave.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___23, adopt=__stack__.all()).inputs, [], [], auto=True)
            invitation.add_inputs(__stack__.all())
            invitation.add_inputs(___23.inputs)
            leave.add_inputs(__stack__.all())
            leave.add_inputs(___23.inputs)
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___13, adopt=__stack__.all()).inputs, [], [], auto=True)
        invitation.add_inputs(__stack__.all())
        invitation.add_inputs(___13.inputs)
        attended.add_inputs(__stack__.all())
        attended.add_inputs(___13.inputs)
        invitations.add_inputs(__stack__.all())
        invitations.add_inputs(___13.inputs)
        leave.add_inputs(__stack__.all())
        leave.add_inputs(___13.inputs)
    if non(___13):
        __stack__.push()
        __stack__.add(___13.inputs)
        leave = Cell('')
        leave.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___13, adopt=__stack__.all()).inputs, [], [], auto=True)
        leave.add_inputs(__stack__.all())
        leave.add_inputs(___13.inputs)
    ___26 = db_str(event[Cell(0)])
    leave = (leave + ((Cell('<tr><td colspan"2"><a href="/2/event/') + ___26) + Cell('">Details</a></td></tr>')))
    leave.add_inputs(__stack__.all())
    __r__ = Cell(((((((((((Cell('<table class="table"><thead><tr><th colspan="2">') + title) + Cell('</th></tr></thead><tbody><tr><td>Description</td><td>')) + description) + Cell('</td></tr><tr><td>Location</td><td>')) + location) + Cell('</td></tr><tr><td>Time/date</td><td>')) + time_date) + Cell('</td></tr>')) + leave) + Cell('</tbody></table>')), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_admin():
    global __stack__
    if ('level' not in locals()):
        level = Cell(None)
    ___27 = meetup.me()
    ___28 = meetup.sql(Cell('SELECT level FROM users WHERE user_id = ?0'), Cell([___27]))
    level = ___28[Cell(0)][Cell(0)]
    level.add_inputs(__stack__.all())
    __r__ = Cell(Cell((level == Cell(3))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_premium():
    global __stack__
    if ('level' not in locals()):
        level = Cell(None)
    ___29 = meetup.me()
    ___30 = meetup.sql(Cell('SELECT level FROM users WHERE user_id = ?0'), Cell([___29]))
    level = ___30[Cell(0)][Cell(0)]
    level.add_inputs(__stack__.all())
    __r__ = Cell(Cell((level >= Cell(2))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_registered():
    global __stack__
    ___31 = meetup.me()
    ___32 = meetup.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([___31]))
    ___33 = db_len(___32)
    __r__ = Cell(Cell((___33 > Cell(0))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_moderator(ev):
    global __stack__
    ___34 = meetup.me()
    ___35 = meetup.sql(Cell('SELECT cat_mod.* FROM cat_mod JOIN ev_cat ON ev_cat.category = cat_mod.category WHERE cat_mod.moderator = ?0 AND ev_cat.event = ?1'), Cell([___34, ev]))
    ___36 = db_len(___35)
    __r__ = Cell(Cell((___36 > Cell(0))), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_manager(ev):
    global __stack__
    ___37 = meetup.me()
    ___38 = meetup.sql(Cell('SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1 AND level = 2'), Cell([ev, ___37]))
    ___39 = db_len(___38)
    ___40 = meetup.sql(Cell('SELECT owner FROM events WHERE id = ?0'), Cell([ev]))
    ___41 = meetup.me()
    __r__ = Cell(Cell((Cell((___39 > Cell(0))).value or Cell((___40[Cell(0)][Cell(0)] == ___41)).value), inputs=dict(Cell((___39 > Cell(0))).inputs)), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def is_attendee(ev):
    global __stack__
    ___42 = meetup.me()
    ___43 = meetup.sql(Cell('SELECT * FROM ev_att WHERE event = ?0 AND attendee = ?1'), Cell([ev, ___42]))
    ___44 = db_len(___43)
    ___45 = meetup.sql(Cell('SELECT owner FROM events WHERE id = ?0'), Cell([ev]))
    ___46 = meetup.me()
    __r__ = Cell(Cell((Cell((___44 > Cell(0))).value or Cell((___45[Cell(0)][Cell(0)] == ___46)).value), inputs=dict(Cell((___44 > Cell(0))).inputs)), adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

def profile():
    global __stack__
    if ('register_html' not in locals()):
        register_html = Cell(None)
    if ('owned_events_html' not in locals()):
        owned_events_html = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('invited_events' not in locals()):
        invited_events = Cell(None)
    if ('inviter' not in locals()):
        inviter = Cell(None)
    if ('html' not in locals()):
        html = Cell(None)
    if ('ev' not in locals()):
        ev = Cell(None)
    if ('attended_events_html' not in locals()):
        attended_events_html = Cell(None)
    if ('owned_events' not in locals()):
        owned_events = Cell(None)
    if ('owned_event' not in locals()):
        owned_event = Cell(None)
    if ('attended_events' not in locals()):
        attended_events = Cell(None)
    if ('managed_events_html' not in locals()):
        managed_events_html = Cell(None)
    if ('attended_event' not in locals()):
        attended_event = Cell(None)
    if ('managed_event' not in locals()):
        managed_event = Cell(None)
    if ('invited_events_html' not in locals()):
        invited_events_html = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('managed_events' not in locals()):
        managed_events = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    if ('unregister_html' not in locals()):
        unregister_html = Cell(None)
    html = Cell('')
    html.add_inputs(__stack__.all())
    header = Cell('<h5 class="card-header">Profile</h5>')
    header.add_inputs(__stack__.all())
    try:
        ___47 = is_registered()[0]
    except Stop as __stop__:
        ev.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        invited_events_html.add_inputs(__stop__.inputs)
        html.add_inputs(__stop__.inputs)
        managed_event.add_inputs(__stop__.inputs)
        invited_events.add_inputs(__stop__.inputs)
        owned_event.add_inputs(__stop__.inputs)
        attended_events_html.add_inputs(__stop__.inputs)
        unregister_html.add_inputs(__stop__.inputs)
        footer.add_inputs(__stop__.inputs)
        inviter.add_inputs(__stop__.inputs)
        attended_events.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        managed_events_html.add_inputs(__stop__.inputs)
        attended_event.add_inputs(__stop__.inputs)
        register_html.add_inputs(__stop__.inputs)
        owned_events_html.add_inputs(__stop__.inputs)
        managed_events.add_inputs(__stop__.inputs)
        owned_events.add_inputs(__stop__.inputs)
        raise __stop__
    ___48 = ___47
    if ___48:
        __stack__.push()
        __stack__.add(___48.inputs)
        owned_events_html = Cell('<div class="card-header">My events</div><div class="card-body"><div class="card-text">')
        owned_events_html.add_inputs(__stack__.all())
        ___49 = meetup.me()
        ___50 = meetup.sql(Cell('SELECT * FROM events WHERE owner = ?0'), Cell([___49]))
        owned_events = ___50
        owned_events.add_inputs(__stack__.all())
        ___51 = db_len(owned_events)
        L = ___51
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___52 = Cell((i < L))
        while ___52:
            __stack__.push()
            __stack__.add(___52.inputs)
            owned_event = owned_events[i]
            owned_event.add_inputs(__stack__.all())
            try:
                ___53 = event_html(owned_event, Cell(False))[0]
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                attended_events_html.add_inputs(__stop__.inputs)
                managed_events_html.add_inputs(__stop__.inputs)
                unregister_html.add_inputs(__stop__.inputs)
                invited_events.add_inputs(__stop__.inputs)
                footer.add_inputs(__stop__.inputs)
                inviter.add_inputs(__stop__.inputs)
                attended_event.add_inputs(__stop__.inputs)
                owned_events_html.add_inputs(__stop__.inputs)
                attended_events.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                managed_events.add_inputs(__stop__.inputs)
                invited_events_html.add_inputs(__stop__.inputs)
                managed_event.add_inputs(__stop__.inputs)
                owned_event.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                raise __stop__
            owned_events_html = (owned_events_html + (Cell('<br>') + ___53))
            owned_events_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___52 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___52, adopt=__stack__.all()).inputs, [], [], auto=True)
        owned_event.add_inputs(__stack__.all())
        owned_event.add_inputs(___52.inputs)
        owned_events_html.add_inputs(__stack__.all())
        owned_events_html.add_inputs(___52.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___52.inputs)
        managed_events_html = Cell('</div></div><div class="card-header">Managed events</div><div class="card-body"><div class="card-text">')
        managed_events_html.add_inputs(__stack__.all())
        ___54 = meetup.me()
        ___55 = meetup.sql(Cell('SELECT events.* FROM events JOIN ev_att ON events.id = ev_att.event WHERE ev_att.attendee = ?0 AND ev_att.level = 2'), Cell([___54]))
        managed_events = ___55
        managed_events.add_inputs(__stack__.all())
        ___56 = db_len(managed_events)
        L = ___56
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___57 = Cell((i < L))
        while ___57:
            __stack__.push()
            __stack__.add(___57.inputs)
            managed_event = managed_events[i]
            managed_event.add_inputs(__stack__.all())
            try:
                ___58 = event_html(managed_event, Cell(False))[0]
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                attended_events_html.add_inputs(__stop__.inputs)
                unregister_html.add_inputs(__stop__.inputs)
                invited_events.add_inputs(__stop__.inputs)
                footer.add_inputs(__stop__.inputs)
                inviter.add_inputs(__stop__.inputs)
                attended_event.add_inputs(__stop__.inputs)
                managed_events_html.add_inputs(__stop__.inputs)
                attended_events.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                invited_events_html.add_inputs(__stop__.inputs)
                managed_event.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                raise __stop__
            managed_events_html = (managed_events_html + (Cell('<br>') + ___58))
            managed_events_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___57 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___57, adopt=__stack__.all()).inputs, [], [], auto=True)
        managed_event.add_inputs(__stack__.all())
        managed_event.add_inputs(___57.inputs)
        managed_events_html.add_inputs(__stack__.all())
        managed_events_html.add_inputs(___57.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___57.inputs)
        attended_events_html = Cell('</div></div><div class="card-header">Attended events</div><div class="card-body"><div class="card-text">')
        attended_events_html.add_inputs(__stack__.all())
        ___59 = meetup.me()
        ___60 = meetup.sql(Cell('SELECT events.* FROM events JOIN ev_att ON events.id = ev_att.event WHERE ev_att.attendee = ?0 AND ev_att.level = 1'), Cell([___59]))
        attended_events = ___60
        attended_events.add_inputs(__stack__.all())
        ___61 = db_len(attended_events)
        L = ___61
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___62 = Cell((i < L))
        while ___62:
            __stack__.push()
            __stack__.add(___62.inputs)
            attended_event = attended_events[i]
            attended_event.add_inputs(__stack__.all())
            try:
                ___63 = event_html(attended_event, Cell(False))[0]
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                unregister_html.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                footer.add_inputs(__stop__.inputs)
                inviter.add_inputs(__stop__.inputs)
                attended_event.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                invited_events_html.add_inputs(__stop__.inputs)
                attended_events_html.add_inputs(__stop__.inputs)
                invited_events.add_inputs(__stop__.inputs)
                raise __stop__
            attended_events_html = (attended_events_html + (Cell('<br>') + ___63))
            attended_events_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___62 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___62, adopt=__stack__.all()).inputs, [], [], auto=True)
        attended_event.add_inputs(__stack__.all())
        attended_event.add_inputs(___62.inputs)
        attended_events_html.add_inputs(__stack__.all())
        attended_events_html.add_inputs(___62.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___62.inputs)
        invited_events_html = Cell('</div></div><div class="card-header">Pending invitations</div><div class="card-body"><div class="card-text">')
        invited_events_html.add_inputs(__stack__.all())
        ___64 = meetup.me()
        ___65 = meetup.sql(Cell('SELECT events.* FROM events JOIN invitations ON events.id = invitations.event WHERE invitations.invitee = ?0'), Cell([___64]))
        invited_events = ___65
        invited_events.add_inputs(__stack__.all())
        ___66 = db_len(invited_events)
        L = ___66
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___67 = Cell((i < L))
        while ___67:
            __stack__.push()
            __stack__.add(___67.inputs)
            ___68 = meetup.sql(Cell('SELECT name FROM users WHERE user_id = ?0'), Cell([invited_events[i][Cell(6)]]))
            inviter = ___68[Cell(0)][Cell(0)]
            inviter.add_inputs(__stack__.all())
            ev = invited_events[i]
            ev.add_inputs(__stack__.all())
            try:
                ___69 = event_html(ev, Cell(True))[0]
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                invited_events_html.add_inputs(__stop__.inputs)
                unregister_html.add_inputs(__stop__.inputs)
                inviter.add_inputs(__stop__.inputs)
                footer.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                raise __stop__
            invited_events_html = (invited_events_html + (((Cell('<br><strong>') + inviter) + Cell('</strong> invited you to ')) + ___69))
            invited_events_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___67 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___67, adopt=__stack__.all()).inputs, [], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___67.inputs)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___67.inputs)
        invited_events_html.add_inputs(__stack__.all())
        invited_events_html.add_inputs(___67.inputs)
        inviter.add_inputs(__stack__.all())
        inviter.add_inputs(___67.inputs)
        unregister_html = Cell('</div></div><div class="card-header">Unregister</div><div class="card-body"><div class="card-text"><a href="/2/unregister">Unregister</a>')
        unregister_html.add_inputs(__stack__.all())
        footer = Cell('</div></div>')
        footer.add_inputs(__stack__.all())
        html = ((((((header + owned_events_html) + managed_events_html) + attended_events_html) + invited_events_html) + unregister_html) + footer)
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___48, adopt=__stack__.all()).inputs, [], [], auto=True)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___48.inputs)
        attended_events_html.add_inputs(__stack__.all())
        attended_events_html.add_inputs(___48.inputs)
        managed_events_html.add_inputs(__stack__.all())
        managed_events_html.add_inputs(___48.inputs)
        unregister_html.add_inputs(__stack__.all())
        unregister_html.add_inputs(___48.inputs)
        footer.add_inputs(__stack__.all())
        footer.add_inputs(___48.inputs)
        inviter.add_inputs(__stack__.all())
        inviter.add_inputs(___48.inputs)
        attended_event.add_inputs(__stack__.all())
        attended_event.add_inputs(___48.inputs)
        owned_events_html.add_inputs(__stack__.all())
        owned_events_html.add_inputs(___48.inputs)
        attended_events.add_inputs(__stack__.all())
        attended_events.add_inputs(___48.inputs)
        html.add_inputs(__stack__.all())
        html.add_inputs(___48.inputs)
        managed_events.add_inputs(__stack__.all())
        managed_events.add_inputs(___48.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___48.inputs)
        owned_events.add_inputs(__stack__.all())
        owned_events.add_inputs(___48.inputs)
        owned_event.add_inputs(__stack__.all())
        owned_event.add_inputs(___48.inputs)
        invited_events_html.add_inputs(__stack__.all())
        invited_events_html.add_inputs(___48.inputs)
        managed_event.add_inputs(__stack__.all())
        managed_event.add_inputs(___48.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___48.inputs)
        invited_events.add_inputs(__stack__.all())
        invited_events.add_inputs(___48.inputs)
    if non(___48):
        __stack__.push()
        __stack__.add(___48.inputs)
        ___70 = meetup.me()
        ___71 = db_str(___70)
        try:
            ___72 = location_select(Cell(0))[0]
        except Stop as __stop__:
            html.add_inputs(__stop__.inputs)
            register_html.add_inputs(__stop__.inputs)
            raise __stop__
        register_html = ((((Cell('<div class="card-header">Register</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/register">\n      <input type="hidden" name="ID" id="ID" value="') + ___71) + Cell('">\n      <div class="form-group mb-1">\n        <label for="name" class="form-label">Name</label>\n        <input type="text" name="name" id="name" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="location" class="form-label">Address</label>\n        ')) + ___72) + Cell('\n      </div>\n      <input type="submit" class="btn btn-primary" value="Submit">\n    </form>\n  </div>\n</div>'))
        register_html.add_inputs(__stack__.all())
        html = (header + register_html)
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___48, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___48.inputs)
        register_html.add_inputs(__stack__.all())
        register_html.add_inputs(___48.inputs)
    try:
        ___73 = make_page(html)[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___73, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/profile')
def _profile():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = profile()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def leave_event(ev):
    global __stack__
    ___74 = meetup.me()
    try:
        ___75 = meetup.sql(Cell('DELETE FROM ev_att WHERE attendee = ?0 AND event = ?1 AND level = 1'), Cell([___74, ev]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___75.inputs, bot=True)
    try:
        ___76 = profile()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___76, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/leave_event/<int:ev>')
def _leave_event(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('leave_event', 'ev', ev)
    (__r__, __s__, __a__, __u__) = leave_event(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def request_attendance(ev):
    global __stack__
    ___77 = meetup.me()
    try:
        ___78 = meetup.sql(Cell('INSERT INTO requests (requester, event) VALUES (?0, ?1)'), Cell([___77, ev]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___78.inputs, bot=True)
    try:
        ___79 = events()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___79, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/request_attendance/<int:ev>')
def _request_attendance(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('request_attendance', 'ev', ev)
    (__r__, __s__, __a__, __u__) = request_attendance(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def reject_invitation(invitation):
    global __stack__
    ___80 = meetup.me()
    try:
        ___81 = meetup.sql(Cell('DELETE FROM invitations WHERE invitee = ?0 AND id = ?1'), Cell([___80, invitation]), stack=__stack__, assigned=['invitations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___81.inputs, bot=True)
    try:
        ___82 = profile()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___82, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/reject_invitation/<int:invitation>')
def _reject_invitation(invitation):
    global __stack__
    __stack__ = Stack()
    invitation = meetup.register('reject_invitation', 'invitation', invitation)
    (__r__, __s__, __a__, __u__) = reject_invitation(invitation)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def accept_invitation(invitation):
    global __stack__
    if ('event_id' not in locals()):
        event_id = Cell(None)
    ___83 = meetup.me()
    ___84 = meetup.sql(Cell('SELECT event FROM invitations WHERE invitee = ?0 AND id = ?1'), Cell([___83, invitation]))
    event_id = ___84
    event_id.add_inputs(__stack__.all())
    event_id = event_id[Cell(0)][Cell(0)]
    event_id.add_inputs(__stack__.all())
    ___85 = meetup.me()
    try:
        ___86 = meetup.sql(Cell('INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)'), Cell([event_id, ___85]), stack=__stack__, assigned=['invitations', 'ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___86.inputs, bot=True)
    ___87 = meetup.me()
    try:
        ___88 = meetup.sql(Cell('DELETE FROM invitations WHERE invitee = ?0 AND id = ?1'), Cell([___87, invitation]), stack=__stack__, assigned=['invitations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___88.inputs, bot=True)
    try:
        ___89 = profile()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___89, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/accept_invitation/<int:invitation>')
def _accept_invitation(invitation):
    global __stack__
    __stack__ = Stack()
    invitation = meetup.register('accept_invitation', 'invitation', invitation)
    (__r__, __s__, __a__, __u__) = accept_invitation(invitation)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def unregister():
    global __stack__
    ___90 = meetup.me()
    try:
        ___91 = meetup.sql(Cell('DELETE FROM users WHERE user_id = ?0'), Cell([___90]), stack=__stack__, assigned=['requests', 'locations', 'cat_mod', 'invitations', 'friends', 'users', 'cat_sub', 'events', 'ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('users', __stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___91.inputs, bot=True)
    ___92 = meetup.me()
    try:
        ___93 = meetup.sql(Cell('DELETE FROM cat_mod WHERE moderator = ?0'), Cell([___92]), stack=__stack__, assigned=['requests', 'locations', 'cat_mod', 'invitations', 'friends', 'cat_sub', 'events', 'ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___93.inputs, bot=True)
    ___94 = meetup.me()
    try:
        ___95 = meetup.sql(Cell('DELETE FROM cat_sub WHERE subscriber = ?0'), Cell([___94]), stack=__stack__, assigned=['requests', 'locations', 'invitations', 'friends', 'cat_sub', 'events', 'ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___95.inputs, bot=True)
    ___96 = meetup.me()
    try:
        ___97 = meetup.sql(Cell('DELETE FROM ev_att WHERE attendee = ?0'), Cell([___96]), stack=__stack__, assigned=['requests', 'locations', 'invitations', 'friends', 'events', 'ev_att'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___97.inputs, bot=True)
    ___98 = meetup.me()
    try:
        ___99 = meetup.sql(Cell('DELETE FROM events WHERE owner = ?0'), Cell([___98]), stack=__stack__, assigned=['requests', 'locations', 'invitations', 'friends', 'events'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___99.inputs, bot=True)
    ___100 = meetup.me()
    try:
        ___101 = meetup.sql(Cell('DELETE FROM friends WHERE user_id = ?0 OR friend_id = ?0'), Cell([___100]), stack=__stack__, assigned=['requests', 'invitations', 'friends', 'locations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('friends', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___101.inputs, bot=True)
    ___102 = meetup.me()
    try:
        ___103 = meetup.sql(Cell('DELETE FROM invitations WHERE inviter = ?0 OR invitee = ?0'), Cell([___102]), stack=__stack__, assigned=['requests', 'invitations', 'locations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___103.inputs, bot=True)
    ___104 = meetup.me()
    try:
        ___105 = meetup.sql(Cell('DELETE FROM locations WHERE owner = ?0'), Cell([___104]), stack=__stack__, assigned=['requests', 'locations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('locations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___105.inputs, bot=True)
    ___106 = meetup.me()
    try:
        ___107 = meetup.sql(Cell('DELETE FROM requests WHERE requester = ?0'), Cell([___106]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___107.inputs, bot=True)
    try:
        ___108 = profile()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___108, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/unregister')
def _unregister():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = unregister()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def register():
    global __stack__
    if ('level' not in locals()):
        level = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('ID' not in locals()):
        ID = Cell(None)
    if ('address' not in locals()):
        address = Cell(None)
    try:
        ___109 = is_registered()[0]
    except Stop as __stop__:
        level.add_inputs(__stop__.inputs)
        ID.add_inputs(__stop__.inputs)
        address.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('users', __stop__.inputs)
        name.add_inputs(__stop__.inputs)
        raise __stop__
    ___110 = non(___109)
    if ___110:
        __stack__.push()
        __stack__.add(___110.inputs)
        ___111 = meetup.me()
        ID = ___111
        ID.add_inputs(__stack__.all())
        ___112 = meetup.get('register', Cell('name'))
        name = ___112
        name.add_inputs(__stack__.all())
        level = Cell(1)
        level.add_inputs(__stack__.all())
        ___113 = meetup.get('register', Cell('location'))
        ___114 = db_int(___113)
        address = ___114
        address.add_inputs(__stack__.all())
        try:
            ___115 = meetup.sql(Cell('INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)'), Cell([ID, name, level, address]), stack=__stack__, assigned=['users'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('users', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___115.inputs, bot=True)
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___110, adopt=__stack__.all()).inputs, ['users'], [], auto=True, u=meetup.me())
        __stack__.add(___110.inputs, bot=True)
        level.add_inputs(__stack__.all())
        level.add_inputs(___110.inputs)
        ID.add_inputs(__stack__.all())
        ID.add_inputs(___110.inputs)
        address.add_inputs(__stack__.all())
        address.add_inputs(___110.inputs)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___110.inputs)
        name.add_inputs(__stack__.all())
        name.add_inputs(___110.inputs)
    try:
        ___116 = profile()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___116, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/register')
def _register():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = register()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def users():
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('table' not in locals()):
        table = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('user' not in locals()):
        user = Cell(None)
    if ('friends' not in locals()):
        friends = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    header = Cell('<h5 class="card-header">Users</h5>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr>\n          <th>ID</th><th>Name</th><th>Level</th><th>Address</th><th>Actions</th>\n        </tr>\n      </thead>\n      <tbody>\n')
    header.add_inputs(__stack__.all())
    table = Cell('')
    table.add_inputs(__stack__.all())
    footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Add friend</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/add_friend">\n      <div class="form-group mb-1">\n        <label for="ID" class="form-label">ID</label>\n        <input type="number" step=1 name="ID" id="ID" class="form-control">\n      </div>\n      <input type="submit" class="btn btn-primary" value="Submit">\n    </form>\n  </div>\n</div>\n')
    footer.add_inputs(__stack__.all())
    try:
        ___117 = is_registered()[0]
    except Stop as __stop__:
        table.add_inputs(__stop__.inputs)
        user.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        friends.add_inputs(__stop__.inputs)
        raise __stop__
    ___118 = ___117
    if ___118:
        __stack__.push()
        __stack__.add(___118.inputs)
        ___119 = meetup.me()
        ___120 = meetup.sql(Cell('SELECT users.* FROM friends LEFT JOIN users ON friends.friend_id = users.user_id WHERE friends.user_id = ?0 OR users.user_id = ?0'), Cell([___119]))
        friends = ___120
        friends.add_inputs(__stack__.all())
        ___121 = db_len(friends)
        L = ___121
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___122 = Cell((i < L))
        while ___122:
            __stack__.push()
            __stack__.add(___122.inputs)
            user = friends[i]
            user.add_inputs(__stack__.all())
            ___123 = db_str(user[Cell(1)])
            table = (table + ((((Cell('<tr><td>') + ___123) + Cell('</td><td>')) + user[Cell(2)]) + Cell('</td><td>')))
            table.add_inputs(__stack__.all())
            ___124 = Cell((user[Cell(3)] == Cell(1)))
            if ___124:
                __stack__.push()
                __stack__.add(___124.inputs)
                table = (table + Cell('free'))
                table.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___124, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___124.inputs)
            if non(___124):
                __stack__.push()
                __stack__.add(___124.inputs)
                ___125 = Cell((user[Cell(3)] == Cell(2)))
                if ___125:
                    __stack__.push()
                    __stack__.add(___125.inputs)
                    table = (table + Cell('premium'))
                    table.add_inputs(__stack__.all())
                    __stack__.pop()
                else:
                    logsanitize(meetup.id_, Cell(___125, adopt=__stack__.all()).inputs, [], [], auto=True)
                    table.add_inputs(__stack__.all())
                    table.add_inputs(___125.inputs)
                if non(___125):
                    __stack__.push()
                    __stack__.add(___125.inputs)
                    ___126 = Cell((user[Cell(3)] == Cell(3)))
                    if ___126:
                        __stack__.push()
                        __stack__.add(___126.inputs)
                        table = (table + Cell('administrator'))
                        table.add_inputs(__stack__.all())
                        __stack__.pop()
                    else:
                        logsanitize(meetup.id_, Cell(___126, adopt=__stack__.all()).inputs, [], [], auto=True)
                        table.add_inputs(__stack__.all())
                        table.add_inputs(___126.inputs)
                    __stack__.pop()
                else:
                    logsanitize(meetup.id_, Cell(___125, adopt=__stack__.all()).inputs, [], [], auto=True)
                    table.add_inputs(__stack__.all())
                    table.add_inputs(___125.inputs)
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___124, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___124.inputs)
            ___127 = Cell((user[Cell(4)] > Cell(0)))
            if ___127:
                __stack__.push()
                __stack__.add(___127.inputs)
                try:
                    ___128 = location_html(user[Cell(4)])[0]
                except Stop as __stop__:
                    i.add_inputs(__stop__.inputs)
                    user.add_inputs(__stop__.inputs)
                    table.add_inputs(__stop__.inputs)
                    raise __stop__
                table = (table + ((Cell('</td><td>') + ___128) + Cell('</td>')))
                table.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___127, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___127.inputs)
            if non(___127):
                __stack__.push()
                __stack__.add(___127.inputs)
                table = (table + Cell('</td><td></td>'))
                table.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___127, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___127.inputs)
            ___129 = meetup.me()
            ___130 = Cell((user[Cell(1)] == ___129))
            if ___130:
                __stack__.push()
                __stack__.add(___130.inputs)
                ___131 = db_str(user[Cell(1)])
                ___132 = db_str(user[Cell(1)])
                table = (table + ((((Cell('<td><a href="/2/update_user/') + ___131) + Cell('">Update</a>&nbsp;<a href="/2/user_categories/')) + ___132) + Cell('">Categories</a></td></tr>')))
                table.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___130, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___130.inputs)
            if non(___130):
                __stack__.push()
                __stack__.add(___130.inputs)
                try:
                    ___133 = is_admin()[0]
                except Stop as __stop__:
                    i.add_inputs(__stop__.inputs)
                    user.add_inputs(__stop__.inputs)
                    table.add_inputs(__stop__.inputs)
                    raise __stop__
                ___134 = ___133
                if ___134:
                    __stack__.push()
                    __stack__.add(___134.inputs)
                    ___135 = db_str(user[Cell(1)])
                    ___136 = db_str(user[Cell(1)])
                    ___137 = db_str(user[Cell(1)])
                    table = (table + ((((((Cell('<td><a href="/2/delete_friend/') + ___135) + Cell('">Delete friend</a>&nbsp;<a href="/2/update_user/')) + ___136) + Cell('">Update</a>&nbsp;<a href="/2/user_categories/')) + ___137) + Cell('">Categories</a></td></tr>')))
                    table.add_inputs(__stack__.all())
                    __stack__.pop()
                else:
                    logsanitize(meetup.id_, Cell(___134, adopt=__stack__.all()).inputs, [], [], auto=True)
                    table.add_inputs(__stack__.all())
                    table.add_inputs(___134.inputs)
                if non(___134):
                    __stack__.push()
                    __stack__.add(___134.inputs)
                    ___138 = db_str(user[Cell(1)])
                    ___139 = db_str(user[Cell(1)])
                    table = (table + ((((Cell('<td><a href="/2/delete_friend/') + ___138) + Cell('">Delete friend</a>&nbsp;<a href="/2/user_categories/')) + ___139) + Cell('">Categories</a></td></tr>')))
                    table.add_inputs(__stack__.all())
                    __stack__.pop()
                else:
                    logsanitize(meetup.id_, Cell(___134, adopt=__stack__.all()).inputs, [], [], auto=True)
                    table.add_inputs(__stack__.all())
                    table.add_inputs(___134.inputs)
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___130, adopt=__stack__.all()).inputs, [], [], auto=True)
                table.add_inputs(__stack__.all())
                table.add_inputs(___130.inputs)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___122 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___122, adopt=__stack__.all()).inputs, [], [], auto=True)
        table.add_inputs(__stack__.all())
        table.add_inputs(___122.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___122.inputs)
        user.add_inputs(__stack__.all())
        user.add_inputs(___122.inputs)
        try:
            ___140 = make_page(((header + table) + footer))[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___140, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___118, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___118.inputs, bot=True)
        table.add_inputs(__stack__.all())
        table.add_inputs(___118.inputs)
        user.add_inputs(__stack__.all())
        user.add_inputs(___118.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___118.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___118.inputs)
        friends.add_inputs(__stack__.all())
        friends.add_inputs(___118.inputs)
    if non(___118):
        __stack__.push()
        __stack__.add(___118.inputs)
        try:
            ___141 = make_page(Cell('<h5 class="card-header">Users</h5>\n<div class="card-body">\n  <div class="card-text">\n    Not available for non-registered users\n  </div>\n</div>'))[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___141, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___118, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___118.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/users')
def _users():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = users()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_friend(user):
    global __stack__
    ___142 = meetup.me()
    try:
        ___143 = meetup.sql(Cell('DELETE FROM friends WHERE user_id = ?0 AND friend_id = ?1'), Cell([___142, user]), stack=__stack__, assigned=['friends'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('friends', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___143.inputs, bot=True)
    try:
        ___144 = users()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___144, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/delete_friend/<int:user>')
def _delete_friend(user):
    global __stack__
    __stack__ = Stack()
    user = meetup.register('delete_friend', 'user', user)
    (__r__, __s__, __a__, __u__) = delete_friend(user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_friend():
    global __stack__
    if ('friend_id' not in locals()):
        friend_id = Cell(None)
    if ('user_id' not in locals()):
        user_id = Cell(None)
    ___145 = meetup.me()
    user_id = ___145
    user_id.add_inputs(__stack__.all())
    ___146 = meetup.get('add_friend', Cell('ID'))
    ___147 = db_int(___146)
    friend_id = ___147
    friend_id.add_inputs(__stack__.all())
    ___148 = meetup.sql(Cell('SELECT * FROM friends WHERE user_id = ?0 AND friend_id = ?1'), Cell([user_id, friend_id]))
    ___149 = db_len(___148)
    ___150 = Cell((___149 == Cell(0)))
    if ___150:
        __stack__.push()
        __stack__.add(___150.inputs)
        ___151 = meetup.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([friend_id]))
        ___152 = db_len(___151)
        ___153 = Cell((___152 > Cell(0)))
        if ___153:
            __stack__.push()
            __stack__.add(___153.inputs)
            try:
                ___154 = meetup.sql(Cell('INSERT INTO friends (user_id, friend_id) VALUES (?0, ?1)'), Cell([user_id, friend_id]), stack=__stack__, assigned=['friends'], called=[meetup.me()])
            except Stop as __stop__:
                meetup.add_sql_inputs('friends', __stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___154.inputs, bot=True)
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___153, adopt=__stack__.all()).inputs, ['friends'], [], auto=True)
            meetup.add_sql_inputs('friends', __stack__.all())
            meetup.add_sql_inputs('friends', ___153.inputs)
        if non(___153):
            __stack__.push()
            __stack__.add(___153.inputs)
            ___155 = db_str(friend_id)
            try:
                ___156 = error_html(((Cell('User ') + ___155) + Cell(' is not registered.<br>\n')))[0]
            except Stop as __stop__:
                raise __stop__
            try:
                ___157 = users()[0]
            except Stop as __stop__:
                raise __stop__
            __r__ = Cell((___156 + ___157), adopt=__stack__.all())
            __s__ = __stack__.all()
            __stack__.pop()
            __stack__.pop()
            return (__r__, __s__, [], [])
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___153, adopt=__stack__.all()).inputs, ['friends'], [], auto=True)
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___150, adopt=__stack__.all()).inputs, ['friends'], [], auto=True, u=meetup.me())
        __stack__.add(___150.inputs, bot=True)
        meetup.add_sql_inputs('friends', __stack__.all())
        meetup.add_sql_inputs('friends', ___150.inputs)
    try:
        ___158 = users()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___158, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/add_friend')
def _add_friend():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = add_friend()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_user(user):
    global __stack__
    if ('premium' not in locals()):
        premium = Cell(None)
    if ('address' not in locals()):
        address = Cell(None)
    if ('free' not in locals()):
        free = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('ID' not in locals()):
        ID = Cell(None)
    if ('administrator' not in locals()):
        administrator = Cell(None)
    ___159 = meetup.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([user]))
    user = ___159[Cell(0)]
    user.add_inputs(__stack__.all())
    ___160 = db_str(user[Cell(0)])
    id_ = ___160
    id_.add_inputs(__stack__.all())
    ___161 = db_str(user[Cell(1)])
    ID = ___161
    ID.add_inputs(__stack__.all())
    name = user[Cell(2)]
    name.add_inputs(__stack__.all())
    ___162 = Cell((user[Cell(3)] == Cell(1)))
    if ___162:
        __stack__.push()
        __stack__.add(___162.inputs)
        free = Cell(' selected')
        free.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___162, adopt=__stack__.all()).inputs, [], [], auto=True)
        free.add_inputs(__stack__.all())
        free.add_inputs(___162.inputs)
    if non(___162):
        __stack__.push()
        __stack__.add(___162.inputs)
        free = Cell('')
        free.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___162, adopt=__stack__.all()).inputs, [], [], auto=True)
        free.add_inputs(__stack__.all())
        free.add_inputs(___162.inputs)
    ___163 = Cell((user[Cell(3)] == Cell(2)))
    if ___163:
        __stack__.push()
        __stack__.add(___163.inputs)
        premium = Cell(' selected')
        premium.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___163, adopt=__stack__.all()).inputs, [], [], auto=True)
        premium.add_inputs(__stack__.all())
        premium.add_inputs(___163.inputs)
    if non(___163):
        __stack__.push()
        __stack__.add(___163.inputs)
        premium = Cell('')
        premium.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___163, adopt=__stack__.all()).inputs, [], [], auto=True)
        premium.add_inputs(__stack__.all())
        premium.add_inputs(___163.inputs)
    ___164 = Cell((user[Cell(3)] == Cell(3)))
    if ___164:
        __stack__.push()
        __stack__.add(___164.inputs)
        administrator = Cell(' selected')
        administrator.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___164, adopt=__stack__.all()).inputs, [], [], auto=True)
        administrator.add_inputs(__stack__.all())
        administrator.add_inputs(___164.inputs)
    if non(___164):
        __stack__.push()
        __stack__.add(___164.inputs)
        administrator = Cell('')
        administrator.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___164, adopt=__stack__.all()).inputs, [], [], auto=True)
        administrator.add_inputs(__stack__.all())
        administrator.add_inputs(___164.inputs)
    address = user[Cell(4)]
    address.add_inputs(__stack__.all())
    try:
        ___165 = location_select(address)[0]
    except Stop as __stop__:
        raise __stop__
    try:
        ___166 = make_page(((((((((((((((Cell('<h5 class="card-header">Update user</h5>\n<div class="card-body">\n  <div class="card-text">\n     <form action="/2/update_user_do">\n       <input type="hidden" name="id_" id="id_" value="') + id_) + Cell('">\n       <div class="form-group mb-1">\n         <label for="ID" class="form-label">ID</label>\n         <input type="number" step=1 name="ID" id="ID" value="')) + ID) + Cell('" class="form-control">\n       </div>\n       <div class="form-group mb-1">\n         <label for="name" class="form-label">Name</label>\n         <input type="text" name="name" id="name" value="')) + name) + Cell('" class="form-control">\n       </div>\n       <div class="form-group mb-1">\n         <label for="level" class="form-label">Level</label>\n         <select name="level" class="form-select">\n           <option value=1')) + free) + Cell('>Free</option>\n           <option value=2')) + premium) + Cell('>Premium</option>\n           <option value=3')) + administrator) + Cell('>Administrator</option>\n         </select>\n       </div>\n       <div class="form-group mb-1">\n         <label for="location" class="form-label">Location</label>\n         ')) + ___165) + Cell('\n       </div>\n       <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/users">Back to users</a>\n</div>\n')))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___166, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/update_user/<int:user>')
def _update_user(user):
    global __stack__
    __stack__ = Stack()
    user = meetup.register('update_user', 'user', user)
    (__r__, __s__, __a__, __u__) = update_user(user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_user_do():
    global __stack__
    if ('level' not in locals()):
        level = Cell(None)
    if ('address' not in locals()):
        address = Cell(None)
    if ('ID' not in locals()):
        ID = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    ___167 = meetup.get('update_user_do', Cell('id_'))
    ___168 = db_int(___167)
    id_ = ___168
    id_.add_inputs(__stack__.all())
    ___169 = meetup.get('update_user_do', Cell('ID'))
    ___170 = db_int(___169)
    ID = ___170
    ID.add_inputs(__stack__.all())
    ___171 = meetup.get('update_user_do', Cell('name'))
    name = ___171
    name.add_inputs(__stack__.all())
    ___172 = meetup.get('update_user_do', Cell('level'))
    ___173 = db_int(___172)
    level = ___173
    level.add_inputs(__stack__.all())
    ___174 = meetup.get('update_user_do', Cell('location'))
    ___175 = db_int(___174)
    address = ___175
    address.add_inputs(__stack__.all())
    try:
        ___176 = is_admin()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('users', __stop__.inputs)
        raise __stop__
    ___177 = meetup.me()
    ___178 = Cell((___176.value or Cell((id_ == ___177)).value), inputs=dict(___176.inputs))
    if ___178:
        __stack__.push()
        __stack__.add(___178.inputs)
        try:
            ___179 = meetup.sql(Cell('DELETE FROM users WHERE id = ?0'), Cell([id_]), stack=__stack__, assigned=['users'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('users', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___179.inputs, bot=True)
        try:
            ___180 = meetup.sql(Cell('INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)'), Cell([ID, name, level, address]), stack=__stack__, assigned=['users'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('users', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___180.inputs, bot=True)
        try:
            ___181 = users()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___181, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___178, adopt=__stack__.all()).inputs, ['users'], [], auto=True, u=meetup.me())
        __stack__.add(___178.inputs, bot=True)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___178.inputs)
    if non(___178):
        __stack__.push()
        __stack__.add(___178.inputs)
        try:
            ___182 = error_html(Cell('Illegal operation: Update user'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___183 = users()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___182 + ___183), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___178, adopt=__stack__.all()).inputs, ['users'], [], auto=True, u=meetup.me())
        __stack__.add(___178.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/update_user_do')
def _update_user_do():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = update_user_do()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def user_categories(user):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('j' not in locals()):
        j = Cell(None)
    if ('ev' not in locals()):
        ev = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('M' not in locals()):
        M = Cell(None)
    if ('usr' not in locals()):
        usr = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    if ('categories_html' not in locals()):
        categories_html = Cell(None)
    ___184 = meetup.sql(Cell('SELECT * FROM users WHERE user_id = ?0'), Cell([user]))
    usr = ___184[Cell(0)]
    usr.add_inputs(__stack__.all())
    header = ((Cell('<h5 class="card-header">Categories of user ') + usr[Cell(2)]) + Cell('</h5>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>Category</th><th>Events</th><th>Actions</th></tr>\n      </thead>\n      <tbody>'))
    header.add_inputs(__stack__.all())
    categories_html = Cell('')
    categories_html.add_inputs(__stack__.all())
    footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/users">Back to users</a>\n</div>')
    footer.add_inputs(__stack__.all())
    ___185 = meetup.sql(Cell('SELECT * FROM categories'))
    categories = ___185
    categories.add_inputs(__stack__.all())
    ___186 = db_len(categories)
    L = ___186
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___187 = Cell((i < L))
    while ___187:
        __stack__.push()
        __stack__.add(___187.inputs)
        category = categories[i]
        category.add_inputs(__stack__.all())
        categories_html = (categories_html + ((Cell('<tr><td>') + category[Cell(1)]) + Cell('</td><td>')))
        categories_html.add_inputs(__stack__.all())
        ___188 = meetup.sql(Cell('SELECT id FROM cat_sub WHERE category = ?0 AND subscriber = ?1'), Cell([category[Cell(0)], user]))
        ___189 = db_len(___188)
        ___190 = Cell((___189 > Cell(0)))
        if ___190:
            __stack__.push()
            __stack__.add(___190.inputs)
            ___191 = meetup.sql(Cell('SELECT events.* FROM events JOIN ev_cat ON ev_cat.event = events.id WHERE ev_cat.category = ?0'), Cell([category[Cell(0)]]))
            events = ___191
            events.add_inputs(__stack__.all())
            ___192 = db_len(events)
            M = ___192
            M.add_inputs(__stack__.all())
            j = Cell(0)
            j.add_inputs(__stack__.all())
            ___193 = Cell((j < M))
            while ___193:
                __stack__.push()
                __stack__.add(___193.inputs)
                ev = events[j]
                ev.add_inputs(__stack__.all())
                try:
                    ___194 = event_html(ev, Cell(True))[0]
                except Stop as __stop__:
                    events.add_inputs(__stop__.inputs)
                    categories_html.add_inputs(__stop__.inputs)
                    i.add_inputs(__stop__.inputs)
                    category.add_inputs(__stop__.inputs)
                    ev.add_inputs(__stop__.inputs)
                    j.add_inputs(__stop__.inputs)
                    M.add_inputs(__stop__.inputs)
                    raise __stop__
                categories_html = (categories_html + (___194 + Cell('<br>')))
                categories_html.add_inputs(__stack__.all())
                j = (j + Cell(1))
                j.add_inputs(__stack__.all())
                __stack__.pop()
                ___193 = Cell((j < M))
            logsanitize(meetup.id_, Cell(___193, adopt=__stack__.all()).inputs, [], [], auto=True)
            j.add_inputs(__stack__.all())
            j.add_inputs(___193.inputs)
            ev.add_inputs(__stack__.all())
            ev.add_inputs(___193.inputs)
            categories_html.add_inputs(__stack__.all())
            categories_html.add_inputs(___193.inputs)
            try:
                ___195 = is_admin()[0]
            except Stop as __stop__:
                events.add_inputs(__stop__.inputs)
                j.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                category.add_inputs(__stop__.inputs)
                ev.add_inputs(__stop__.inputs)
                categories_html.add_inputs(__stop__.inputs)
                M.add_inputs(__stop__.inputs)
                raise __stop__
            ___196 = meetup.me()
            ___197 = Cell((___195.value or Cell((user == ___196)).value), inputs=dict(___195.inputs))
            if ___197:
                __stack__.push()
                __stack__.add(___197.inputs)
                ___198 = db_str(category[Cell(0)])
                ___199 = db_str(user)
                categories_html = (categories_html + ((((Cell('</td><td><a href="/2/unsubscribe/') + ___198) + Cell('/')) + ___199) + Cell('">Unsubscribe</a></td></tr>')))
                categories_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___197, adopt=__stack__.all()).inputs, [], [], auto=True)
                categories_html.add_inputs(__stack__.all())
                categories_html.add_inputs(___197.inputs)
            if non(___197):
                __stack__.push()
                __stack__.add(___197.inputs)
                categories_html = (categories_html + Cell('</td><td></td></tr>'))
                categories_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___197, adopt=__stack__.all()).inputs, [], [], auto=True)
                categories_html.add_inputs(__stack__.all())
                categories_html.add_inputs(___197.inputs)
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___190, adopt=__stack__.all()).inputs, [], [], auto=True)
            events.add_inputs(__stack__.all())
            events.add_inputs(___190.inputs)
            j.add_inputs(__stack__.all())
            j.add_inputs(___190.inputs)
            categories_html.add_inputs(__stack__.all())
            categories_html.add_inputs(___190.inputs)
            ev.add_inputs(__stack__.all())
            ev.add_inputs(___190.inputs)
            M.add_inputs(__stack__.all())
            M.add_inputs(___190.inputs)
        if non(___190):
            __stack__.push()
            __stack__.add(___190.inputs)
            try:
                ___200 = is_admin()[0]
            except Stop as __stop__:
                categories_html.add_inputs(__stop__.inputs)
                events.add_inputs(__stop__.inputs)
                j.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                category.add_inputs(__stop__.inputs)
                ev.add_inputs(__stop__.inputs)
                M.add_inputs(__stop__.inputs)
                raise __stop__
            ___201 = meetup.me()
            ___202 = Cell((___200.value or Cell((user == ___201)).value), inputs=dict(___200.inputs))
            if ___202:
                __stack__.push()
                __stack__.add(___202.inputs)
                ___203 = db_str(category[Cell(0)])
                ___204 = db_str(user)
                categories_html = (categories_html + ((((Cell('</td><td><a href="/2/subscribe/') + ___203) + Cell('/')) + ___204) + Cell('">Subscribe</a></td></tr>')))
                categories_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___202, adopt=__stack__.all()).inputs, [], [], auto=True)
                categories_html.add_inputs(__stack__.all())
                categories_html.add_inputs(___202.inputs)
            if non(___202):
                __stack__.push()
                __stack__.add(___202.inputs)
                categories_html = (categories_html + Cell('</td><td></td></tr>'))
                categories_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___202, adopt=__stack__.all()).inputs, [], [], auto=True)
                categories_html.add_inputs(__stack__.all())
                categories_html.add_inputs(___202.inputs)
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___190, adopt=__stack__.all()).inputs, [], [], auto=True)
            categories_html.add_inputs(__stack__.all())
            categories_html.add_inputs(___190.inputs)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___187 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___187, adopt=__stack__.all()).inputs, [], [], auto=True)
    events.add_inputs(__stack__.all())
    events.add_inputs(___187.inputs)
    categories_html.add_inputs(__stack__.all())
    categories_html.add_inputs(___187.inputs)
    j.add_inputs(__stack__.all())
    j.add_inputs(___187.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___187.inputs)
    category.add_inputs(__stack__.all())
    category.add_inputs(___187.inputs)
    ev.add_inputs(__stack__.all())
    ev.add_inputs(___187.inputs)
    M.add_inputs(__stack__.all())
    M.add_inputs(___187.inputs)
    try:
        ___205 = make_page(((header + categories_html) + footer))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___205, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/user_categories/<int:user>')
def _user_categories(user):
    global __stack__
    __stack__ = Stack()
    user = meetup.register('user_categories', 'user', user)
    (__r__, __s__, __a__, __u__) = user_categories(user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def unsubscribe(category, user):
    global __stack__
    try:
        ___206 = is_admin()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        raise __stop__
    ___207 = meetup.me()
    ___208 = Cell((___206.value or Cell((user == ___207)).value), inputs=dict(___206.inputs))
    if ___208:
        __stack__.push()
        __stack__.add(___208.inputs)
        try:
            ___209 = meetup.sql(Cell('DELETE FROM cat_sub WHERE category = ?0 AND subscriber = ?1'), Cell([category, user]), stack=__stack__, assigned=['cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___209.inputs, bot=True)
        try:
            ___210 = user_categories(user)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___210, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___208, adopt=__stack__.all()).inputs, ['cat_sub'], [], auto=True, u=meetup.me())
        __stack__.add(___208.inputs, bot=True)
        meetup.add_sql_inputs('cat_sub', __stack__.all())
        meetup.add_sql_inputs('cat_sub', ___208.inputs)
    if non(___208):
        __stack__.push()
        __stack__.add(___208.inputs)
        try:
            ___211 = error_html(Cell('Illegal operation: Unsubscribe'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___212 = user_categories(user)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___211 + ___212), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___208, adopt=__stack__.all()).inputs, ['cat_sub'], [], auto=True, u=meetup.me())
        __stack__.add(___208.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/unsubscribe/<int:category>/<int:user>')
def _unsubscribe(category, user):
    global __stack__
    __stack__ = Stack()
    category = meetup.register('unsubscribe', 'category', category)
    user = meetup.register('unsubscribe', 'user', user)
    (__r__, __s__, __a__, __u__) = unsubscribe(category, user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def subscribe(category, user):
    global __stack__
    if ('level' not in locals()):
        level = Cell(None)
    if ('subscriptions' not in locals()):
        subscriptions = Cell(None)
    try:
        ___213 = is_admin()[0]
    except Stop as __stop__:
        level.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        subscriptions.add_inputs(__stop__.inputs)
        raise __stop__
    ___214 = meetup.me()
    ___215 = Cell((___213.value or Cell((user == ___214)).value), inputs=dict(___213.inputs))
    if ___215:
        __stack__.push()
        __stack__.add(___215.inputs)
        ___216 = meetup.sql(Cell('SELECT level FROM users WHERE user_id = ?0'), Cell([user]))
        level = ___216[Cell(0)][Cell(0)]
        level.add_inputs(__stack__.all())
        ___217 = Cell((level == Cell(1)))
        if ___217:
            __stack__.push()
            __stack__.add(___217.inputs)
            ___218 = meetup.sql(Cell('SELECT * FROM cat_sub WHERE subscriber = ?0'), Cell([user]))
            subscriptions = ___218
            subscriptions.add_inputs(__stack__.all())
            ___219 = db_len(subscriptions)
            ___220 = Cell((___219 > Cell(2)))
            if ___220:
                __stack__.push()
                __stack__.add(___220.inputs)
                try:
                    ___221 = user_categories(user)[0]
                except Stop as __stop__:
                    raise __stop__
                __r__ = Cell((Cell('Illegal operation: Subscribe<br>\n') + ___221), adopt=__stack__.all())
                __s__ = __stack__.all()
                __stack__.pop()
                __stack__.pop()
                __stack__.pop()
                return (__r__, __s__, [], [])
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___220, adopt=__stack__.all()).inputs, [], [], auto=True)
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___217, adopt=__stack__.all()).inputs, [], [], auto=True)
            subscriptions.add_inputs(__stack__.all())
            subscriptions.add_inputs(___217.inputs)
        try:
            ___222 = meetup.sql(Cell('INSERT INTO cat_sub (category, subscriber) VALUES (?0, ?1)'), Cell([category, user]), stack=__stack__, assigned=['cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___222.inputs, bot=True)
        try:
            ___223 = user_categories(user)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___223, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___215, adopt=__stack__.all()).inputs, ['cat_sub'], [], auto=True, u=meetup.me())
        __stack__.add(___215.inputs, bot=True)
        level.add_inputs(__stack__.all())
        level.add_inputs(___215.inputs)
        meetup.add_sql_inputs('cat_sub', __stack__.all())
        meetup.add_sql_inputs('cat_sub', ___215.inputs)
        subscriptions.add_inputs(__stack__.all())
        subscriptions.add_inputs(___215.inputs)
    if non(___215):
        __stack__.push()
        __stack__.add(___215.inputs)
        try:
            ___224 = error_html(Cell('Illegal operation: Subscribe'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___225 = user_categories(user)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___224 + ___225), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___215, adopt=__stack__.all()).inputs, ['cat_sub'], [], auto=True, u=meetup.me())
        __stack__.add(___215.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/subscribe/<int:category>/<int:user>')
def _subscribe(category, user):
    global __stack__
    __stack__ = Stack()
    category = meetup.register('subscribe', 'category', category)
    user = meetup.register('subscribe', 'user', user)
    (__r__, __s__, __a__, __u__) = subscribe(category, user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def categories():
    global __stack__
    if ('table' not in locals()):
        table = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('cat' not in locals()):
        cat = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    header = Cell('<h5 class="card-header">Categories</h5>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n')
    header.add_inputs(__stack__.all())
    table = Cell('')
    table.add_inputs(__stack__.all())
    try:
        ___226 = is_admin()[0]
    except Stop as __stop__:
        cat.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        footer.add_inputs(__stop__.inputs)
        header.add_inputs(__stop__.inputs)
        categories.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        table.add_inputs(__stop__.inputs)
        raise __stop__
    ___227 = ___226
    if ___227:
        __stack__.push()
        __stack__.add(___227.inputs)
        footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Add new category</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/add_category">\n      <div class="form-group mb-1">\n        <label for="name" class="form-label">Name</label>\n        <input type="text" name="name" id="name" class="form-control">\n      </div>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n')
        footer.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___227, adopt=__stack__.all()).inputs, [], [], auto=True)
        footer.add_inputs(__stack__.all())
        footer.add_inputs(___227.inputs)
    if non(___227):
        __stack__.push()
        __stack__.add(___227.inputs)
        footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>')
        footer.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___227, adopt=__stack__.all()).inputs, [], [], auto=True)
        footer.add_inputs(__stack__.all())
        footer.add_inputs(___227.inputs)
    ___228 = meetup.me()
    ___229 = meetup.sql(Cell('SELECT categories.* FROM friends LEFT JOIN categories ON categories.owner = friends.friend_id WHERE friends.user_id = ?0 OR categories.owner = ?0'), Cell([___228]))
    categories = ___229
    categories.add_inputs(__stack__.all())
    ___230 = db_len(categories)
    L = ___230
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___231 = Cell((i < L))
    while ___231:
        __stack__.push()
        __stack__.add(___231.inputs)
        cat = categories[i]
        cat.add_inputs(__stack__.all())
        try:
            ___232 = is_admin()[0]
        except Stop as __stop__:
            cat.add_inputs(__stop__.inputs)
            table.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            raise __stop__
        ___233 = ___232
        if ___233:
            __stack__.push()
            __stack__.add(___233.inputs)
            ___234 = db_str(cat[Cell(1)])
            ___235 = db_str(cat[Cell(0)])
            ___236 = db_str(cat[Cell(0)])
            ___237 = db_str(cat[Cell(0)])
            table = (table + ((((((((Cell('<tr><td>') + ___234) + Cell('</td><td><a href="/2/delete_category/')) + ___235) + Cell('">Delete</a>&nbsp;<a href="/2/update_category/')) + ___236) + Cell('">Update</a>&nbsp;<a href="/2/category/')) + ___237) + Cell('">Details</a></td></tr>')))
            table.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___233, adopt=__stack__.all()).inputs, [], [], auto=True)
            table.add_inputs(__stack__.all())
            table.add_inputs(___233.inputs)
        if non(___233):
            __stack__.push()
            __stack__.add(___233.inputs)
            ___238 = db_str(cat[Cell(1)])
            table = (table + ((Cell('<tr><td>') + ___238) + Cell('</td><td></td></tr>')))
            table.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___233, adopt=__stack__.all()).inputs, [], [], auto=True)
            table.add_inputs(__stack__.all())
            table.add_inputs(___233.inputs)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___231 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___231, adopt=__stack__.all()).inputs, [], [], auto=True)
    cat.add_inputs(__stack__.all())
    cat.add_inputs(___231.inputs)
    table.add_inputs(__stack__.all())
    table.add_inputs(___231.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___231.inputs)
    try:
        ___239 = make_page(((header + table) + footer))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___239, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/categories')
def _categories():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = categories()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_category(cat):
    global __stack__
    try:
        ___240 = is_admin()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        meetup.add_sql_inputs('categories', __stop__.inputs)
        raise __stop__
    ___241 = ___240
    if ___241:
        __stack__.push()
        __stack__.add(___241.inputs)
        try:
            ___242 = meetup.sql(Cell('DELETE FROM categories WHERE id = ?0'), Cell([cat]), stack=__stack__, assigned=['cat_mod', 'ev_cat', 'cat_sub', 'categories'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            meetup.add_sql_inputs('categories', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___242.inputs, bot=True)
        try:
            ___243 = meetup.sql(Cell('DELETE FROM cat_mod WHERE category = ?0'), Cell([cat]), stack=__stack__, assigned=['cat_mod', 'ev_cat', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___243.inputs, bot=True)
        try:
            ___244 = meetup.sql(Cell('DELETE FROM cat_sub WHERE category = ?0'), Cell([cat]), stack=__stack__, assigned=['ev_cat', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___244.inputs, bot=True)
        try:
            ___245 = meetup.sql(Cell('DELETE FROM ev_cat WHERE category = ?0'), Cell([cat]), stack=__stack__, assigned=['ev_cat'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___245.inputs, bot=True)
        try:
            ___246 = categories()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___246, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___241, adopt=__stack__.all()).inputs, ['cat_mod', 'ev_cat', 'cat_sub', 'categories'], [], auto=True, u=meetup.me())
        __stack__.add(___241.inputs, bot=True)
        meetup.add_sql_inputs('cat_mod', __stack__.all())
        meetup.add_sql_inputs('cat_mod', ___241.inputs)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___241.inputs)
        meetup.add_sql_inputs('cat_sub', __stack__.all())
        meetup.add_sql_inputs('cat_sub', ___241.inputs)
        meetup.add_sql_inputs('categories', __stack__.all())
        meetup.add_sql_inputs('categories', ___241.inputs)
    if non(___241):
        __stack__.push()
        __stack__.add(___241.inputs)
        try:
            ___247 = error_html(Cell('Illegal operation: Delete category'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___248 = categories()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___247 + ___248), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___241, adopt=__stack__.all()).inputs, ['cat_mod', 'ev_cat', 'cat_sub', 'categories'], [], auto=True, u=meetup.me())
        __stack__.add(___241.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/delete_category/<int:cat>')
def _delete_category(cat):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('delete_category', 'cat', cat)
    (__r__, __s__, __a__, __u__) = delete_category(cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_category():
    global __stack__
    if ('name' not in locals()):
        name = Cell(None)
    try:
        ___249 = is_admin()[0]
    except Stop as __stop__:
        name.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('categories', __stop__.inputs)
        raise __stop__
    ___250 = ___249
    if ___250:
        __stack__.push()
        __stack__.add(___250.inputs)
        ___251 = meetup.get('add_category', Cell('name'))
        name = ___251
        name.add_inputs(__stack__.all())
        ___252 = meetup.me()
        try:
            ___253 = meetup.sql(Cell('INSERT INTO categories (name, owner) VALUES (?0, ?1)'), Cell([name, ___252]), stack=__stack__, assigned=['categories'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('categories', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___253.inputs, bot=True)
        try:
            ___254 = categories()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___254, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___250, adopt=__stack__.all()).inputs, ['categories'], [], auto=True, u=meetup.me())
        __stack__.add(___250.inputs, bot=True)
        name.add_inputs(__stack__.all())
        name.add_inputs(___250.inputs)
        meetup.add_sql_inputs('categories', __stack__.all())
        meetup.add_sql_inputs('categories', ___250.inputs)
    if non(___250):
        __stack__.push()
        __stack__.add(___250.inputs)
        try:
            ___255 = error_html(Cell('Illegal operation: Add category'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___256 = categories()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___255 + ___256), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___250, adopt=__stack__.all()).inputs, ['categories'], [], auto=True, u=meetup.me())
        __stack__.add(___250.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/add_category')
def _add_category():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = add_category()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_category(cat):
    global __stack__
    if ('cat_' not in locals()):
        cat_ = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    ___257 = meetup.sql(Cell('SELECT * FROM categories WHERE id = ?0'), Cell([cat]))
    cat_ = ___257[Cell(0)]
    cat_.add_inputs(__stack__.all())
    ___258 = db_str(cat_[Cell(0)])
    id_ = ___258
    id_.add_inputs(__stack__.all())
    name = cat_[Cell(1)]
    name.add_inputs(__stack__.all())
    try:
        ___259 = make_page(((((Cell('<h5 class="card-header">Update category</h5>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/update_category_do">\n      <input type="hidden" name="id_" id="id_" value="') + id_) + Cell('">\n      <div class="form-group mb-1">\n        <label for="name" class="form-label">Name</label>\n        <input type="text" name="name" id="name" value="')) + name) + Cell('" class="form-control">\n      </div>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/categories">Back to categories</a>\n</div>\n')))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___259, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/update_category/<int:cat>')
def _update_category(cat):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('update_category', 'cat', cat)
    (__r__, __s__, __a__, __u__) = update_category(cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_category_do():
    global __stack__
    if ('cat_mods' not in locals()):
        cat_mods = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('ev_cat' not in locals()):
        ev_cat = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('new_id' not in locals()):
        new_id = Cell(None)
    if ('ev_cats' not in locals()):
        ev_cats = Cell(None)
    if ('cat_sub' not in locals()):
        cat_sub = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('cat_mod' not in locals()):
        cat_mod = Cell(None)
    if ('cat_subs' not in locals()):
        cat_subs = Cell(None)
    try:
        ___260 = is_admin()[0]
    except Stop as __stop__:
        new_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        ev_cats.add_inputs(__stop__.inputs)
        cat_mod.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('categories', __stop__.inputs)
        name.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        L.add_inputs(__stop__.inputs)
        cat_subs.add_inputs(__stop__.inputs)
        owner.add_inputs(__stop__.inputs)
        id_.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        ev_cat.add_inputs(__stop__.inputs)
        cat_sub.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        cat_mods.add_inputs(__stop__.inputs)
        raise __stop__
    ___261 = non(___260)
    if ___261:
        __stack__.push()
        __stack__.add(___261.inputs)
        try:
            ___262 = error_html(Cell('Illegal operation: Update category'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___263 = categories()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___262 + ___263), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___261, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___261.inputs, bot=True)
    ___264 = meetup.get('update_category_do', Cell('id_'))
    ___265 = db_int(___264)
    id_ = ___265
    id_.add_inputs(__stack__.all())
    ___266 = meetup.get('update_category_do', Cell('name'))
    name = ___266
    name.add_inputs(__stack__.all())
    ___267 = meetup.sql(Cell('SELECT owner FROM categories WHERE id = ?0'), Cell([id_]))
    owner = ___267[Cell(0)][Cell(0)]
    owner.add_inputs(__stack__.all())
    try:
        ___268 = meetup.sql(Cell('DELETE FROM categories WHERE id = ?0'), Cell([id_]), stack=__stack__, assigned=['ev_cat', 'categories', 'cat_mod', 'cat_sub'], called=[meetup.me()])
    except Stop as __stop__:
        new_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        ev_cats.add_inputs(__stop__.inputs)
        cat_mod.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('categories', __stop__.inputs)
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        L.add_inputs(__stop__.inputs)
        cat_subs.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        ev_cat.add_inputs(__stop__.inputs)
        cat_sub.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        cat_mods.add_inputs(__stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___268.inputs, bot=True)
    try:
        ___269 = meetup.sql(Cell('INSERT INTO categories (name, owner) VALUES (?0, ?1)'), Cell([name, owner]), stack=__stack__, assigned=['ev_cat', 'categories', 'cat_mod', 'cat_sub'], called=[meetup.me()])
    except Stop as __stop__:
        new_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        ev_cats.add_inputs(__stop__.inputs)
        cat_mod.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('categories', __stop__.inputs)
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        L.add_inputs(__stop__.inputs)
        cat_subs.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('cat_sub', __stop__.inputs)
        ev_cat.add_inputs(__stop__.inputs)
        cat_sub.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        cat_mods.add_inputs(__stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___269.inputs, bot=True)
    new_id = ___269[Cell(0)]
    new_id.add_inputs(__stack__.all())
    ___270 = meetup.sql(Cell('SELECT * FROM cat_mod WHERE category = ?0'), Cell([id_]))
    cat_mods = ___270
    cat_mods.add_inputs(__stack__.all())
    ___271 = db_len(cat_mods)
    L = ___271
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___272 = Cell((i < L))
    while ___272:
        __stack__.push()
        __stack__.add(___272.inputs)
        cat_mod = cat_mods[i]
        cat_mod.add_inputs(__stack__.all())
        try:
            ___273 = meetup.sql(Cell('DELETE FROM cat_mod WHERE id = ?0'), Cell([cat_mod[Cell(0)]]), stack=__stack__, assigned=['ev_cat', 'cat_mod', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            cat_mod.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            i.add_inputs(__stop__.inputs)
            cat_subs.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            cat_sub.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___273.inputs, bot=True)
        try:
            ___274 = meetup.sql(Cell('INSERT INTO cat_mod (category, moderator) VALUES (?0, ?1)'), Cell([new_id, cat_mod[Cell(2)]]), stack=__stack__, assigned=['ev_cat', 'cat_mod', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            cat_mod.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            i.add_inputs(__stop__.inputs)
            cat_subs.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            cat_sub.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___274.inputs, bot=True)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___272 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___272, adopt=__stack__.all()).inputs, ['cat_mod'], [], auto=True, u=meetup.me())
    __stack__.add(___272.inputs, bot=True)
    meetup.add_sql_inputs('cat_mod', __stack__.all())
    meetup.add_sql_inputs('cat_mod', ___272.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___272.inputs)
    cat_mod.add_inputs(__stack__.all())
    cat_mod.add_inputs(___272.inputs)
    ___275 = meetup.sql(Cell('SELECT * FROM cat_sub WHERE category = ?0'), Cell([id_]))
    cat_subs = ___275
    cat_subs.add_inputs(__stack__.all())
    ___276 = db_len(cat_subs)
    L = ___276
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___277 = Cell((i < L))
    while ___277:
        __stack__.push()
        __stack__.add(___277.inputs)
        cat_sub = cat_subs[i]
        cat_sub.add_inputs(__stack__.all())
        try:
            ___278 = meetup.sql(Cell('DELETE FROM cat_sub WHERE id = ?0'), Cell([cat_sub[Cell(0)]]), stack=__stack__, assigned=['ev_cat', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            cat_sub.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___278.inputs, bot=True)
        try:
            ___279 = meetup.sql(Cell('INSERT INTO cat_sub (category, subscriber) VALUES (?0, ?1)'), Cell([new_id, cat_sub[Cell(2)]]), stack=__stack__, assigned=['ev_cat', 'cat_sub'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('cat_sub', __stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            cat_sub.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___279.inputs, bot=True)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___277 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___277, adopt=__stack__.all()).inputs, ['cat_sub'], [], auto=True, u=meetup.me())
    __stack__.add(___277.inputs, bot=True)
    cat_sub.add_inputs(__stack__.all())
    cat_sub.add_inputs(___277.inputs)
    meetup.add_sql_inputs('cat_sub', __stack__.all())
    meetup.add_sql_inputs('cat_sub', ___277.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___277.inputs)
    ___280 = meetup.sql(Cell('SELECT * FROM ev_cat WHERE category = ?0'), Cell([id_]))
    ev_cats = ___280
    ev_cats.add_inputs(__stack__.all())
    ___281 = db_len(ev_cats)
    L = ___281
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___282 = Cell((i < L))
    while ___282:
        __stack__.push()
        __stack__.add(___282.inputs)
        ev_cat = ev_cats[i]
        ev_cat.add_inputs(__stack__.all())
        try:
            ___283 = meetup.sql(Cell('DELETE FROM ev_cat WHERE id = ?0'), Cell([ev_cat[Cell(0)]]), stack=__stack__, assigned=['ev_cat'], called=[meetup.me()])
        except Stop as __stop__:
            i.add_inputs(__stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___283.inputs, bot=True)
        try:
            ___284 = meetup.sql(Cell('INSERT INTO ev_cat (event, category) VALUES (?0, ?1)'), Cell([ev_cat[Cell(1)], new_id]), stack=__stack__, assigned=['ev_cat'], called=[meetup.me()])
        except Stop as __stop__:
            i.add_inputs(__stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___284.inputs, bot=True)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___282 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___282, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True, u=meetup.me())
    __stack__.add(___282.inputs, bot=True)
    i.add_inputs(__stack__.all())
    i.add_inputs(___282.inputs)
    ev_cat.add_inputs(__stack__.all())
    ev_cat.add_inputs(___282.inputs)
    meetup.add_sql_inputs('ev_cat', __stack__.all())
    meetup.add_sql_inputs('ev_cat', ___282.inputs)
    try:
        ___285 = categories()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___285, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/update_category_do')
def _update_category_do():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = update_category_do()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def category(cat):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('subscribers_html' not in locals()):
        subscribers_html = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('moderators_html' not in locals()):
        moderators_html = Cell(None)
    if ('moderators' not in locals()):
        moderators = Cell(None)
    if ('moderator' not in locals()):
        moderator = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('subscribers' not in locals()):
        subscribers = Cell(None)
    if ('subscriber' not in locals()):
        subscriber = Cell(None)
    if ('events_html' not in locals()):
        events_html = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    if ('is_subscriber' not in locals()):
        is_subscriber = Cell(None)
    ___286 = meetup.sql(Cell('SELECT name FROM categories WHERE id = ?0'), Cell([cat]))
    name = ___286[Cell(0)][Cell(0)]
    name.add_inputs(__stack__.all())
    header = ((Cell('<h5 class="card-header">Category ') + name) + Cell('</h5>'))
    header.add_inputs(__stack__.all())
    ___287 = meetup.me()
    ___288 = meetup.sql(Cell('SELECT * FROM cat_sub WHERE category = ?0 AND subscriber = ?1'), Cell([cat, ___287]))
    ___289 = db_len(___288)
    is_subscriber = Cell((___289 > Cell(0)))
    is_subscriber.add_inputs(__stack__.all())
    moderators_html = Cell('')
    moderators_html.add_inputs(__stack__.all())
    subscribers_html = Cell('')
    subscribers_html.add_inputs(__stack__.all())
    ___290 = is_subscriber
    if ___290:
        __stack__.push()
        __stack__.add(___290.inputs)
        moderators_html = Cell('<div class="card-header">Moderators</div>')
        moderators_html.add_inputs(__stack__.all())
        try:
            ___291 = is_admin()[0]
        except Stop as __stop__:
            moderator.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            subscribers_html.add_inputs(__stop__.inputs)
            events.add_inputs(__stop__.inputs)
            subscribers.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            footer.add_inputs(__stop__.inputs)
            subscriber.add_inputs(__stop__.inputs)
            moderators.add_inputs(__stop__.inputs)
            events_html.add_inputs(__stop__.inputs)
            moderators_html.add_inputs(__stop__.inputs)
            raise __stop__
        try:
            ___292 = is_moderator(cat)[0]
        except Stop as __stop__:
            moderator.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            subscribers_html.add_inputs(__stop__.inputs)
            events.add_inputs(__stop__.inputs)
            subscribers.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            footer.add_inputs(__stop__.inputs)
            subscriber.add_inputs(__stop__.inputs)
            moderators.add_inputs(__stop__.inputs)
            events_html.add_inputs(__stop__.inputs)
            moderators_html.add_inputs(__stop__.inputs)
            raise __stop__
        ___293 = Cell((___291.value or ___292.value), inputs=dict(___291.inputs))
        if ___293:
            __stack__.push()
            __stack__.add(___293.inputs)
            ___294 = db_str(cat)
            moderators_html = (moderators_html + ((Cell('\n<div class="card-body">\n  <a href="/2/category_moderators/') + ___294) + Cell('">Modify</a>\n</div>')))
            moderators_html.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___293, adopt=__stack__.all()).inputs, [], [], auto=True)
            moderators_html.add_inputs(__stack__.all())
            moderators_html.add_inputs(___293.inputs)
        moderators_html = (moderators_html + Cell('\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th></tr>\n      </thead>\n      <tbody>\n'))
        moderators_html.add_inputs(__stack__.all())
        ___295 = meetup.sql(Cell('SELECT users.* FROM users JOIN cat_mod ON cat_mod.moderator = users.id WHERE cat_mod.category = ?0'), Cell([cat]))
        moderators = ___295
        moderators.add_inputs(__stack__.all())
        ___296 = db_len(moderators)
        L = ___296
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___297 = Cell((i < L))
        while ___297:
            __stack__.push()
            __stack__.add(___297.inputs)
            moderator = moderators[i]
            moderator.add_inputs(__stack__.all())
            ___298 = db_str(moderator[Cell(1)])
            moderators_html = (moderators_html + ((((Cell('<tr><td>') + ___298) + Cell('</td><td>')) + moderator[Cell(2)]) + Cell('</td></tr>')))
            moderators_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___297 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___297, adopt=__stack__.all()).inputs, [], [], auto=True)
        moderator.add_inputs(__stack__.all())
        moderator.add_inputs(___297.inputs)
        moderators_html.add_inputs(__stack__.all())
        moderators_html.add_inputs(___297.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___297.inputs)
        subscribers_html = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Subscribers</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th></tr>\n      </thead>\n      <tbody>\n')
        subscribers_html.add_inputs(__stack__.all())
        ___299 = meetup.sql(Cell('SELECT users.* FROM users JOIN cat_sub ON cat_sub.subscriber = users.id WHERE cat_sub.category = ?0'), Cell([cat]))
        subscribers = ___299
        subscribers.add_inputs(__stack__.all())
        ___300 = db_len(subscribers)
        L = ___300
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___301 = Cell((i < L))
        while ___301:
            __stack__.push()
            __stack__.add(___301.inputs)
            subscriber = subscribers[i]
            subscriber.add_inputs(__stack__.all())
            ___302 = db_str(subscriber[Cell(1)])
            subscribers_html = (subscribers_html + ((((Cell('<tr><td>') + ___302) + Cell('</td><td>')) + subscriber[Cell(2)]) + Cell('</td></tr>')))
            subscribers_html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___301 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___301, adopt=__stack__.all()).inputs, [], [], auto=True)
        subscribers_html.add_inputs(__stack__.all())
        subscribers_html.add_inputs(___301.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___301.inputs)
        subscriber.add_inputs(__stack__.all())
        subscriber.add_inputs(___301.inputs)
        events_html = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Events</div>\n<div class="card-body">\n  <div class="card-text">\n')
        events_html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___290, adopt=__stack__.all()).inputs, [], [], auto=True)
        moderator.add_inputs(__stack__.all())
        moderator.add_inputs(___290.inputs)
        subscribers_html.add_inputs(__stack__.all())
        subscribers_html.add_inputs(___290.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___290.inputs)
        moderators_html.add_inputs(__stack__.all())
        moderators_html.add_inputs(___290.inputs)
        subscribers.add_inputs(__stack__.all())
        subscribers.add_inputs(___290.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___290.inputs)
        subscriber.add_inputs(__stack__.all())
        subscriber.add_inputs(___290.inputs)
        moderators.add_inputs(__stack__.all())
        moderators.add_inputs(___290.inputs)
        events_html.add_inputs(__stack__.all())
        events_html.add_inputs(___290.inputs)
    if non(___290):
        __stack__.push()
        __stack__.add(___290.inputs)
        events_html = Cell('\n<div class="card-header">Events</div>\n<div class="card-body">\n  <div class="card-text">\n')
        events_html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___290, adopt=__stack__.all()).inputs, [], [], auto=True)
        events_html.add_inputs(__stack__.all())
        events_html.add_inputs(___290.inputs)
    ___303 = meetup.sql(Cell('SELECT events.* FROM events JOIN ev_cat ON ev_cat.event = events.id WHERE ev_cat.category = ?0'), Cell([cat]))
    events = ___303
    events.add_inputs(__stack__.all())
    ___304 = db_len(events)
    L = ___304
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___305 = Cell((i < L))
    while ___305:
        __stack__.push()
        __stack__.add(___305.inputs)
        try:
            ___306 = event_html(events[i], Cell(True))[0]
        except Stop as __stop__:
            events_html.add_inputs(__stop__.inputs)
            footer.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            raise __stop__
        events_html = (events_html + ___306)
        events_html.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___305 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___305, adopt=__stack__.all()).inputs, [], [], auto=True)
    events_html.add_inputs(__stack__.all())
    events_html.add_inputs(___305.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___305.inputs)
    footer = Cell('\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/categories">Back to categories</a>\n</div>')
    footer.add_inputs(__stack__.all())
    try:
        ___307 = make_page(((((header + moderators_html) + subscribers_html) + events_html) + footer))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___307, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/category/<int:cat>')
def _category(cat):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('category', 'cat', cat)
    (__r__, __s__, __a__, __u__) = category(cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def category_moderators(cat):
    global __stack__
    if ('current_html' not in locals()):
        current_html = Cell(None)
    if ('L' not in locals()):
        L = Cell(None)
    if ('footer1' not in locals()):
        footer1 = Cell(None)
    if ('footer2' not in locals()):
        footer2 = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('new_html' not in locals()):
        new_html = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    if ('user' not in locals()):
        user = Cell(None)
    try:
        ___308 = is_admin()[0]
    except Stop as __stop__:
        user.add_inputs(__stop__.inputs)
        new_html.add_inputs(__stop__.inputs)
        header.add_inputs(__stop__.inputs)
        name.add_inputs(__stop__.inputs)
        footer2.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        current_html.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        footer1.add_inputs(__stop__.inputs)
        users.add_inputs(__stop__.inputs)
        raise __stop__
    ___309 = ___308
    if ___309:
        __stack__.push()
        __stack__.add(___309.inputs)
        ___310 = meetup.sql(Cell('SELECT name FROM categories WHERE id = ?0'), Cell([cat]))
        name = ___310[Cell(0)][Cell(0)]
        name.add_inputs(__stack__.all())
        header = ((Cell('<h5 class="card-header">Moderators of category ') + name) + Cell('</h5>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n'))
        header.add_inputs(__stack__.all())
        current_html = Cell('')
        current_html.add_inputs(__stack__.all())
        footer1 = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Add new moderators</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n')
        footer1.add_inputs(__stack__.all())
        new_html = Cell('')
        new_html.add_inputs(__stack__.all())
        ___311 = db_str(cat)
        footer2 = ((Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/category/') + ___311) + Cell('">Back to category</a>\n</div>'))
        footer2.add_inputs(__stack__.all())
        ___312 = meetup.sql(Cell('SELECT id, user_id, name FROM users'), Cell([cat]))
        users = ___312
        users.add_inputs(__stack__.all())
        ___313 = db_len(users)
        L = ___313
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___314 = Cell((i < L))
        while ___314:
            __stack__.push()
            __stack__.add(___314.inputs)
            user = users[i]
            user.add_inputs(__stack__.all())
            ___315 = meetup.sql(Cell('SELECT * FROM cat_mod WHERE category = ?0 AND moderator = ?1'), Cell([cat, user[Cell(0)]]))
            ___316 = db_len(___315)
            ___317 = Cell((___316 > Cell(0)))
            if ___317:
                __stack__.push()
                __stack__.add(___317.inputs)
                ___318 = db_str(user[Cell(1)])
                ___319 = db_str(cat)
                ___320 = db_str(user[Cell(0)])
                current_html = (current_html + ((((((((Cell('<tr><td>') + ___318) + Cell('</td><td>')) + user[Cell(2)]) + Cell('</td><td><a href="/2/delete_category_moderator/')) + ___319) + Cell('/')) + ___320) + Cell('">Remove moderator</a></td></tr>')))
                current_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___317, adopt=__stack__.all()).inputs, [], [], auto=True)
                current_html.add_inputs(__stack__.all())
                current_html.add_inputs(___317.inputs)
            if non(___317):
                __stack__.push()
                __stack__.add(___317.inputs)
                ___321 = db_str(user[Cell(1)])
                ___322 = db_str(cat)
                ___323 = db_str(user[Cell(0)])
                new_html = (new_html + ((((((((Cell('<tr><td>') + ___321) + Cell('</td><td>')) + user[Cell(2)]) + Cell('</td><td><a href="/2/add_category_moderator/')) + ___322) + Cell('/')) + ___323) + Cell('">Make moderator</a></td></tr>')))
                new_html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___317, adopt=__stack__.all()).inputs, [], [], auto=True)
                new_html.add_inputs(__stack__.all())
                new_html.add_inputs(___317.inputs)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___314 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___314, adopt=__stack__.all()).inputs, [], [], auto=True)
        new_html.add_inputs(__stack__.all())
        new_html.add_inputs(___314.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___314.inputs)
        current_html.add_inputs(__stack__.all())
        current_html.add_inputs(___314.inputs)
        user.add_inputs(__stack__.all())
        user.add_inputs(___314.inputs)
        try:
            ___324 = make_page(((((header + current_html) + footer1) + new_html) + footer2))[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___324, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___309, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___309.inputs, bot=True)
        user.add_inputs(__stack__.all())
        user.add_inputs(___309.inputs)
        new_html.add_inputs(__stack__.all())
        new_html.add_inputs(___309.inputs)
        header.add_inputs(__stack__.all())
        header.add_inputs(___309.inputs)
        name.add_inputs(__stack__.all())
        name.add_inputs(___309.inputs)
        footer2.add_inputs(__stack__.all())
        footer2.add_inputs(___309.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___309.inputs)
        current_html.add_inputs(__stack__.all())
        current_html.add_inputs(___309.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___309.inputs)
        footer1.add_inputs(__stack__.all())
        footer1.add_inputs(___309.inputs)
        users.add_inputs(__stack__.all())
        users.add_inputs(___309.inputs)
    if non(___309):
        __stack__.push()
        __stack__.add(___309.inputs)
        try:
            ___325 = error_html(Cell('Illegal operation: Category moderators'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___326 = category(cat)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___325 + ___326), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___309, adopt=__stack__.all()).inputs, [], [], auto=True, u=meetup.me())
        __stack__.add(___309.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/category_moderators/<int:cat>')
def _category_moderators(cat):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('category_moderators', 'cat', cat)
    (__r__, __s__, __a__, __u__) = category_moderators(cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_category_moderator(cat, user):
    global __stack__
    try:
        ___327 = is_admin()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        raise __stop__
    ___328 = ___327
    if ___328:
        __stack__.push()
        __stack__.add(___328.inputs)
        try:
            ___329 = meetup.sql(Cell('DELETE FROM cat_mod WHERE category = ?0 AND moderator = ?1'), Cell([cat, user]), stack=__stack__, assigned=['cat_mod'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___329.inputs, bot=True)
        try:
            ___330 = category_moderators(cat)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___330, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___328, adopt=__stack__.all()).inputs, ['cat_mod'], [], auto=True, u=meetup.me())
        __stack__.add(___328.inputs, bot=True)
        meetup.add_sql_inputs('cat_mod', __stack__.all())
        meetup.add_sql_inputs('cat_mod', ___328.inputs)
    if non(___328):
        __stack__.push()
        __stack__.add(___328.inputs)
        try:
            ___331 = error_html(Cell('Illegal operation: Delete category moderator'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___332 = category(cat)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___331 + ___332), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___328, adopt=__stack__.all()).inputs, ['cat_mod'], [], auto=True, u=meetup.me())
        __stack__.add(___328.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/delete_category_moderator/<int:cat>/<int:user>')
def _delete_category_moderator(cat, user):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('delete_category_moderator', 'cat', cat)
    user = meetup.register('delete_category_moderator', 'user', user)
    (__r__, __s__, __a__, __u__) = delete_category_moderator(cat, user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_category_moderator(cat, user):
    global __stack__
    try:
        ___333 = is_admin()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('cat_mod', __stop__.inputs)
        raise __stop__
    ___334 = ___333
    if ___334:
        __stack__.push()
        __stack__.add(___334.inputs)
        try:
            ___335 = meetup.sql(Cell('INSERT INTO cat_mod (category, moderator) VALUES (?0, ?1)'), Cell([cat, user]), stack=__stack__, assigned=['cat_mod'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('cat_mod', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___335.inputs, bot=True)
        try:
            ___336 = category_moderators(cat)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___336, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___334, adopt=__stack__.all()).inputs, ['cat_mod'], [], auto=True, u=meetup.me())
        __stack__.add(___334.inputs, bot=True)
        meetup.add_sql_inputs('cat_mod', __stack__.all())
        meetup.add_sql_inputs('cat_mod', ___334.inputs)
    if non(___334):
        __stack__.push()
        __stack__.add(___334.inputs)
        try:
            ___337 = error_html(Cell('Illegal operation: Add category moderator'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___338 = category(cat)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___337 + ___338), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___334, adopt=__stack__.all()).inputs, ['cat_mod'], [], auto=True, u=meetup.me())
        __stack__.add(___334.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/add_category_moderator/<int:cat>/<int:user>')
def _add_category_moderator(cat, user):
    global __stack__
    __stack__ = Stack()
    cat = meetup.register('add_category_moderator', 'cat', cat)
    user = meetup.register('add_category_moderator', 'user', user)
    (__r__, __s__, __a__, __u__) = add_category_moderator(cat, user)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def events():
    global __stack__
    try:
        ___339 = events_from(Cell(0))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___339, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/events')
def _events():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = events()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def events_from(start):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('ev' not in locals()):
        ev = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('L2' not in locals()):
        L2 = Cell(None)
    if ('events_html' not in locals()):
        events_html = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    header = Cell('<h5 class="card-header">Events</h5>\n<div class="card-body">\n  <div class="card-text">\n')
    header.add_inputs(__stack__.all())
    events_html = Cell('')
    events_html.add_inputs(__stack__.all())
    try:
        ___340 = location_select(Cell(0))[0]
    except Stop as __stop__:
        events.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        ev.add_inputs(__stop__.inputs)
        events_html.add_inputs(__stop__.inputs)
        footer.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        L2.add_inputs(__stop__.inputs)
        raise __stop__
    footer = ((Cell('\n  </div>\n</div>\n<div class="card-header">Add new event</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/add_event">\n      <div class="form-group mb-1">\n        <label for="title" class="form-label">Title</label>\n        <input type="text" name="title" id="title" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="description" class="form-label">Description</label>\n        <input type="text" name="description" id="description" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="location" class="form-label">Location</label>\n        ') + ___340) + Cell('\n      </div>\n      <div class="form-group mb-1">\n        <label for="time" class="form-label">Time</label>\n        <input type="text" name="time" id="time" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="date" class="form-label">Date</label>\n        <input type="text" name="date" id="date" class="form-control">\n      </div>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n'))
    footer.add_inputs(__stack__.all())
    ___341 = meetup.me()
    ___342 = meetup.sql(Cell('SELECT events.* FROM events LEFT JOIN friends ON events.owner = friends.friend_id WHERE friends.user_id = ?0 OR events.owner = ?0 ORDER BY events.id DESC LIMIT 5 OFFSET ?1'), Cell([___341, start]))
    events = ___342
    events.add_inputs(__stack__.all())
    ___343 = meetup.me()
    ___344 = meetup.sql(Cell('SELECT events.id FROM events LEFT JOIN friends ON events.owner = friends.friend_id WHERE friends.user_id = ?0 OR events.owner = ?0 LIMIT 6 OFFSET ?1'), Cell([___343, start]))
    ___345 = db_len(___344)
    L = ___345
    L.add_inputs(__stack__.all())
    ___346 = db_len(events)
    L2 = ___346
    L2.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___347 = Cell((i < L2))
    while ___347:
        __stack__.push()
        __stack__.add(___347.inputs)
        ev = events[i]
        ev.add_inputs(__stack__.all())
        try:
            ___348 = event_html(ev, Cell(True))[0]
        except Stop as __stop__:
            ev.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            events_html.add_inputs(__stop__.inputs)
            raise __stop__
        events_html = (events_html + (___348 + Cell('<br>')))
        events_html.add_inputs(__stack__.all())
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___347 = Cell((i < L2))
    logsanitize(meetup.id_, Cell(___347, adopt=__stack__.all()).inputs, [], [], auto=True)
    i.add_inputs(__stack__.all())
    i.add_inputs(___347.inputs)
    ev.add_inputs(__stack__.all())
    ev.add_inputs(___347.inputs)
    events_html.add_inputs(__stack__.all())
    events_html.add_inputs(___347.inputs)
    ___349 = Cell((Cell((start > Cell(0))).value or Cell((L > Cell(5))).value), inputs=dict(Cell((start > Cell(0))).inputs))
    if ___349:
        __stack__.push()
        __stack__.add(___349.inputs)
        events_html = (Cell('  </ul>\n</nav>') + events_html)
        events_html.add_inputs(__stack__.all())
        ___350 = Cell((L > Cell(5)))
        if ___350:
            __stack__.push()
            __stack__.add(___350.inputs)
            ___351 = db_str((start + Cell(5)))
            ___352 = db_str((start + Cell(6)))
            events_html = (((((Cell('<li class="page-item"><a class="page-link" href="/2/events/') + ___351) + Cell('">Events ')) + ___352) + Cell('-...</a></li>')) + events_html)
            events_html.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___350, adopt=__stack__.all()).inputs, [], [], auto=True)
            events_html.add_inputs(__stack__.all())
            events_html.add_inputs(___350.inputs)
        ___353 = db_str((start + Cell(1)))
        ___354 = db_str((start + Cell(5)))
        events_html = (((((Cell('<li class="page-item active"><a class="page-link" href="#">Events ') + ___353) + Cell('-')) + ___354) + Cell('</a></li>')) + events_html)
        events_html.add_inputs(__stack__.all())
        ___355 = Cell((start > Cell(0)))
        if ___355:
            __stack__.push()
            __stack__.add(___355.inputs)
            ___356 = db_str((start - Cell(5)))
            ___357 = db_str((start - Cell(4)))
            ___358 = db_str(start)
            events_html = (((((((Cell('<li class="page-item"><a class="page-link" href="/2/events/') + ___356) + Cell('">Events ')) + ___357) + Cell('-')) + ___358) + Cell('</a></li>')) + events_html)
            events_html.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___355, adopt=__stack__.all()).inputs, [], [], auto=True)
            events_html.add_inputs(__stack__.all())
            events_html.add_inputs(___355.inputs)
        events_html = (Cell('<nav>\n  <ul class="pagination">') + events_html)
        events_html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___349, adopt=__stack__.all()).inputs, [], [], auto=True)
        events_html.add_inputs(__stack__.all())
        events_html.add_inputs(___349.inputs)
    try:
        ___359 = make_page(((header + events_html) + footer))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___359, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/events/<int:start>')
def _events_from(start):
    global __stack__
    __stack__ = Stack()
    start = meetup.register('events_from', 'start', start)
    (__r__, __s__, __a__, __u__) = events_from(start)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_event():
    global __stack__
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    if ('level' not in locals()):
        level = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('date' not in locals()):
        date = Cell(None)
    if ('description' not in locals()):
        description = Cell(None)
    if ('owned' not in locals()):
        owned = Cell(None)
    if ('time' not in locals()):
        time = Cell(None)
    ___360 = meetup.get('add_event', Cell('title'))
    title = ___360
    title.add_inputs(__stack__.all())
    ___361 = meetup.get('add_event', Cell('description'))
    description = ___361
    description.add_inputs(__stack__.all())
    ___362 = meetup.get('add_event', Cell('location'))
    ___363 = db_int(___362)
    location = ___363
    location.add_inputs(__stack__.all())
    ___364 = meetup.get('add_event', Cell('time'))
    time = ___364
    time.add_inputs(__stack__.all())
    ___365 = meetup.get('add_event', Cell('date'))
    date = ___365
    date.add_inputs(__stack__.all())
    ___366 = meetup.me()
    owner = ___366
    owner.add_inputs(__stack__.all())
    ___367 = meetup.me()
    ___368 = meetup.sql(Cell('SELECT level FROM users WHERE user_id = ?0'), Cell([___367]))
    level = ___368[Cell(0)][Cell(0)]
    level.add_inputs(__stack__.all())
    ___369 = meetup.me()
    ___370 = meetup.sql(Cell('SELECT * FROM events WHERE owner = ?0 LIMIT 3'), Cell([___369]))
    ___371 = db_len(___370)
    owned = ___371
    owned.add_inputs(__stack__.all())
    ___372 = Cell((Cell((level == Cell(1))).value and Cell((owned > Cell(2))).value), inputs=dict(Cell((level == Cell(1))).inputs))
    if ___372:
        __stack__.push()
        __stack__.add(___372.inputs)
        try:
            ___373 = error_html(Cell('Illegal operation: Add event'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___374 = events()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___373 + ___374), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___372, adopt=__stack__.all()).inputs, ['events'], [], auto=True, u=meetup.me())
        __stack__.add(___372.inputs, bot=True)
    if non(___372):
        __stack__.push()
        __stack__.add(___372.inputs)
        try:
            ___375 = meetup.sql(Cell('INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)'), Cell([title, description, location, time, date, owner]), stack=__stack__, assigned=['events'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('events', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___375.inputs, bot=True)
        try:
            ___376 = events()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___376, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___372, adopt=__stack__.all()).inputs, ['events'], [], auto=True, u=meetup.me())
        __stack__.add(___372.inputs, bot=True)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___372.inputs)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/add_event')
def _add_event():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = add_event()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def event(ev):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('evt' not in locals()):
        evt = Cell(None)
    if ('html' not in locals()):
        html = Cell(None)
    if ('attendees' not in locals()):
        attendees = Cell(None)
    if ('manager' not in locals()):
        manager = Cell(None)
    if ('requester' not in locals()):
        requester = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('cat' not in locals()):
        cat = Cell(None)
    if ('managers' not in locals()):
        managers = Cell(None)
    if ('requesters' not in locals()):
        requesters = Cell(None)
    if ('cats' not in locals()):
        cats = Cell(None)
    if ('is_event_category' not in locals()):
        is_event_category = Cell(None)
    if ('attendee' not in locals()):
        attendee = Cell(None)
    ___377 = meetup.sql(Cell('SELECT * FROM events WHERE id = ?0'), Cell([ev]))
    evt = ___377[Cell(0)]
    evt.add_inputs(__stack__.all())
    try:
        ___378 = event_html(evt, Cell(True))[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        cats.add_inputs(__stop__.inputs)
        manager.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        requester.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        cat.add_inputs(__stop__.inputs)
        attendees.add_inputs(__stop__.inputs)
        managers.add_inputs(__stop__.inputs)
        is_event_category.add_inputs(__stop__.inputs)
        requesters.add_inputs(__stop__.inputs)
        attendee.add_inputs(__stop__.inputs)
        raise __stop__
    html = ((Cell('<h5 class="card-header">Event</h5>\n<div class="card-body">\n  <div class="card-text">\n    ') + ___378) + Cell('\n  </div>\n</div>\n<div class="card-header">Managers</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n'))
    html.add_inputs(__stack__.all())
    ___379 = meetup.sql(Cell('SELECT users.user_id, users.name FROM users JOIN ev_att ON ev_att.attendee = users.user_id WHERE ev_att.event = ?0 AND ev_att.level = 2'), Cell([ev]))
    managers = ___379
    managers.add_inputs(__stack__.all())
    ___380 = db_len(managers)
    L = ___380
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___381 = Cell((i < L))
    while ___381:
        __stack__.push()
        __stack__.add(___381.inputs)
        manager = managers[i]
        manager.add_inputs(__stack__.all())
        ___382 = db_str(manager[Cell(0)])
        html = (html + ((((Cell('<tr><td>') + ___382) + Cell('</td><td>')) + manager[Cell(1)]) + Cell('</td>')))
        html.add_inputs(__stack__.all())
        ___383 = meetup.me()
        try:
            ___384 = is_premium()[0]
        except Stop as __stop__:
            cats.add_inputs(__stop__.inputs)
            manager.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            requester.add_inputs(__stop__.inputs)
            cat.add_inputs(__stop__.inputs)
            requesters.add_inputs(__stop__.inputs)
            attendees.add_inputs(__stop__.inputs)
            is_event_category.add_inputs(__stop__.inputs)
            html.add_inputs(__stop__.inputs)
            attendee.add_inputs(__stop__.inputs)
            raise __stop__
        ___385 = Cell((Cell((evt[Cell(6)] == ___383)).value and ___384.value), inputs=dict(Cell((evt[Cell(6)] == ___383)).inputs))
        if ___385:
            __stack__.push()
            __stack__.add(___385.inputs)
            ___386 = db_str(ev)
            ___387 = db_str(manager[Cell(0)])
            html = (html + ((((Cell('<td><a href="/2/revoke_moderator/') + ___386) + Cell('/')) + ___387) + Cell('">Revoke</a></td></tr>')))
            html.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___385, adopt=__stack__.all()).inputs, [], [], auto=True)
            html.add_inputs(__stack__.all())
            html.add_inputs(___385.inputs)
        if non(___385):
            __stack__.push()
            __stack__.add(___385.inputs)
            html = (html + Cell('<td></td></tr>'))
            html.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___385, adopt=__stack__.all()).inputs, [], [], auto=True)
            html.add_inputs(__stack__.all())
            html.add_inputs(___385.inputs)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___381 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___381, adopt=__stack__.all()).inputs, [], [], auto=True)
    manager.add_inputs(__stack__.all())
    manager.add_inputs(___381.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___381.inputs)
    html.add_inputs(__stack__.all())
    html.add_inputs(___381.inputs)
    try:
        ___388 = is_attendee(ev)[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        cats.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        requester.add_inputs(__stop__.inputs)
        cat.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        attendees.add_inputs(__stop__.inputs)
        is_event_category.add_inputs(__stop__.inputs)
        requesters.add_inputs(__stop__.inputs)
        attendee.add_inputs(__stop__.inputs)
        raise __stop__
    try:
        ___389 = is_manager(ev)[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        cats.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        requester.add_inputs(__stop__.inputs)
        cat.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        attendees.add_inputs(__stop__.inputs)
        is_event_category.add_inputs(__stop__.inputs)
        requesters.add_inputs(__stop__.inputs)
        attendee.add_inputs(__stop__.inputs)
        raise __stop__
    try:
        ___390 = is_premium()[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        cats.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        requester.add_inputs(__stop__.inputs)
        cat.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        attendees.add_inputs(__stop__.inputs)
        is_event_category.add_inputs(__stop__.inputs)
        requesters.add_inputs(__stop__.inputs)
        attendee.add_inputs(__stop__.inputs)
        raise __stop__
    ___391 = Cell((___388.value or Cell((___389.value or ___390.value), inputs=dict(___389.inputs)).value), inputs=dict(___388.inputs))
    if ___391:
        __stack__.push()
        __stack__.add(___391.inputs)
        html = (html + Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Attendees</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n'))
        html.add_inputs(__stack__.all())
        ___392 = meetup.sql(Cell('SELECT users.user_id, users.name FROM users JOIN ev_att ON ev_att.attendee = users.user_id WHERE ev_att.event = ?0 AND ev_att.level = 1'), Cell([ev]))
        attendees = ___392
        attendees.add_inputs(__stack__.all())
        ___393 = db_len(attendees)
        L = ___393
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___394 = Cell((i < L))
        while ___394:
            __stack__.push()
            __stack__.add(___394.inputs)
            attendee = attendees[i]
            attendee.add_inputs(__stack__.all())
            ___395 = db_str(attendee[Cell(0)])
            html = (html + ((((Cell('<tr><td>') + ___395) + Cell('</td><td>')) + attendee[Cell(1)]) + Cell('</td>')))
            html.add_inputs(__stack__.all())
            try:
                ___396 = is_manager(ev)[0]
            except Stop as __stop__:
                cats.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                requester.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                cat.add_inputs(__stop__.inputs)
                is_event_category.add_inputs(__stop__.inputs)
                requesters.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                attendee.add_inputs(__stop__.inputs)
                raise __stop__
            ___397 = meetup.me()
            try:
                ___398 = is_premium()[0]
            except Stop as __stop__:
                cats.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                requester.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                cat.add_inputs(__stop__.inputs)
                is_event_category.add_inputs(__stop__.inputs)
                requesters.add_inputs(__stop__.inputs)
                html.add_inputs(__stop__.inputs)
                attendee.add_inputs(__stop__.inputs)
                raise __stop__
            ___399 = Cell((___396.value or Cell((Cell((evt[Cell(6)] == ___397)).value and ___398.value), inputs=dict(Cell((evt[Cell(6)] == ___397)).inputs)).value), inputs=dict(___396.inputs))
            if ___399:
                __stack__.push()
                __stack__.add(___399.inputs)
                ___400 = db_str(ev)
                ___401 = db_str(attendee[Cell(0)])
                html = (html + ((((Cell('<td><a href="/2/promote_attendee/') + ___400) + Cell('/')) + ___401) + Cell('">Promote to manager</a></td></tr>')))
                html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___399, adopt=__stack__.all()).inputs, [], [], auto=True)
                html.add_inputs(__stack__.all())
                html.add_inputs(___399.inputs)
            if non(___399):
                __stack__.push()
                __stack__.add(___399.inputs)
                html = (html + Cell('<td></td></tr>'))
                html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___399, adopt=__stack__.all()).inputs, [], [], auto=True)
                html.add_inputs(__stack__.all())
                html.add_inputs(___399.inputs)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___394 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___394, adopt=__stack__.all()).inputs, [], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___394.inputs)
        html.add_inputs(__stack__.all())
        html.add_inputs(___394.inputs)
        attendee.add_inputs(__stack__.all())
        attendee.add_inputs(___394.inputs)
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___391, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___391.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___391.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___391.inputs)
        attendees.add_inputs(__stack__.all())
        attendees.add_inputs(___391.inputs)
        attendee.add_inputs(__stack__.all())
        attendee.add_inputs(___391.inputs)
    try:
        ___402 = is_manager(ev)[0]
    except Stop as __stop__:
        cats.add_inputs(__stop__.inputs)
        requester.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        cat.add_inputs(__stop__.inputs)
        requesters.add_inputs(__stop__.inputs)
        html.add_inputs(__stop__.inputs)
        is_event_category.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        raise __stop__
    ___403 = ___402
    if ___403:
        __stack__.push()
        __stack__.add(___403.inputs)
        html = (html + Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Attendance requests</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>ID</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n'))
        html.add_inputs(__stack__.all())
        ___404 = meetup.sql(Cell('SELECT users.user_id, users.name FROM users JOIN requests ON requests.requester = users.user_id WHERE requests.event = ?0'), Cell([ev]))
        requesters = ___404
        requesters.add_inputs(__stack__.all())
        ___405 = db_len(requesters)
        L = ___405
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___406 = Cell((i < L))
        while ___406:
            __stack__.push()
            __stack__.add(___406.inputs)
            requester = requesters[i]
            requester.add_inputs(__stack__.all())
            ___407 = db_str(requester[Cell(0)])
            ___408 = db_str(requester[Cell(1)])
            ___409 = db_str(ev)
            ___410 = db_str(requester[Cell(0)])
            ___411 = db_str(ev)
            ___412 = db_str(requester[Cell(0)])
            html = (html + ((((((((((((Cell('<tr><td>') + ___407) + Cell('</td><td>')) + ___408) + Cell('</td><td><a href="/2/accept_request/')) + ___409) + Cell('/')) + ___410) + Cell('">Accept</a>&nbsp;<a href="/2/reject_request/')) + ___411) + Cell('/')) + ___412) + Cell('">Reject</a>&nbsp;</td></tr>')))
            html.add_inputs(__stack__.all())
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___406 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___406, adopt=__stack__.all()).inputs, [], [], auto=True)
        requester.add_inputs(__stack__.all())
        requester.add_inputs(___406.inputs)
        html.add_inputs(__stack__.all())
        html.add_inputs(___406.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___406.inputs)
        html = (html + Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Categories</div>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n'))
        html.add_inputs(__stack__.all())
        ___413 = meetup.me()
        ___414 = meetup.sql(Cell('SELECT categories.* FROM categories LEFT JOIN friends ON friends.friend_id = categories.owner WHERE friends.user_id = ?0 OR categories.owner = ?0'), Cell([___413]))
        cats = ___414
        cats.add_inputs(__stack__.all())
        ___415 = db_len(cats)
        L = ___415
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___416 = Cell((i < L))
        while ___416:
            __stack__.push()
            __stack__.add(___416.inputs)
            cat = cats[i]
            cat.add_inputs(__stack__.all())
            ___417 = meetup.sql(Cell('SELECT * FROM ev_cat WHERE event = ?0 AND category = ?1'), Cell([ev, cat[Cell(0)]]))
            ___418 = db_len(___417)
            is_event_category = Cell((___418 > Cell(0)))
            is_event_category.add_inputs(__stack__.all())
            ___419 = is_event_category
            if ___419:
                __stack__.push()
                __stack__.add(___419.inputs)
                ___420 = db_str(cat[Cell(1)])
                ___421 = db_str(ev)
                ___422 = db_str(cat[Cell(0)])
                html = (html + ((((((Cell('<tr><td>') + ___420) + Cell(' (selected)</td><td><a href="/2/delete_event_category/')) + ___421) + Cell('/')) + ___422) + Cell('">Delete</td></tr>')))
                html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___419, adopt=__stack__.all()).inputs, [], [], auto=True)
                html.add_inputs(__stack__.all())
                html.add_inputs(___419.inputs)
            if non(___419):
                __stack__.push()
                __stack__.add(___419.inputs)
                ___423 = db_str(cat[Cell(1)])
                ___424 = db_str(ev)
                ___425 = db_str(cat[Cell(0)])
                html = (html + ((((((Cell('<tr><td>') + ___423) + Cell('</td><td><a href="/2/add_event_category/')) + ___424) + Cell('/')) + ___425) + Cell('">Add</td></tr>')))
                html.add_inputs(__stack__.all())
                __stack__.pop()
            else:
                logsanitize(meetup.id_, Cell(___419, adopt=__stack__.all()).inputs, [], [], auto=True)
                html.add_inputs(__stack__.all())
                html.add_inputs(___419.inputs)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___416 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___416, adopt=__stack__.all()).inputs, [], [], auto=True)
        is_event_category.add_inputs(__stack__.all())
        is_event_category.add_inputs(___416.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___416.inputs)
        html.add_inputs(__stack__.all())
        html.add_inputs(___416.inputs)
        cat.add_inputs(__stack__.all())
        cat.add_inputs(___416.inputs)
        ___426 = db_str(ev)
        ___427 = db_str(ev)
        html = (html + ((((Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Actions</div>\n<div class="card-body">\n  <div class="card-text">\n    <a href="/2/update_event/') + ___426) + Cell('">Update</a>&nbsp;<a href="/2/delete_event/')) + ___427) + Cell('">Delete</a><br>\n')))
        html.add_inputs(__stack__.all())
        ___428 = db_str(ev)
        html = (html + ((Cell('\n  </div>\n</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/invite/') + ___428) + Cell('" class="row">\n      <div class="col-auto">\n        <input type="text" readonly class="form-control-plaintext" value="Invite user with ID">\n      </div>\n      <div class="col-auto">\n        <input type="number" step=1 name="ID" id="ID" class="form-control">\n      </div>\n      <div class="col-auto">\n        <input type="submit" value="Submit" class="btn btn-primary">\n      </div>\n    </form>\n  </div>\n</div>\n')))
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___403, adopt=__stack__.all()).inputs, [], [], auto=True)
        cats.add_inputs(__stack__.all())
        cats.add_inputs(___403.inputs)
        requester.add_inputs(__stack__.all())
        requester.add_inputs(___403.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___403.inputs)
        cat.add_inputs(__stack__.all())
        cat.add_inputs(___403.inputs)
        requesters.add_inputs(__stack__.all())
        requesters.add_inputs(___403.inputs)
        html.add_inputs(__stack__.all())
        html.add_inputs(___403.inputs)
        is_event_category.add_inputs(__stack__.all())
        is_event_category.add_inputs(___403.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___403.inputs)
    try:
        ___429 = is_moderator(ev)[0]
    except Stop as __stop__:
        html.add_inputs(__stop__.inputs)
        raise __stop__
    ___430 = ___429
    if ___430:
        __stack__.push()
        __stack__.add(___430.inputs)
        ___431 = db_str(ev)
        html = (html + ((Cell('\n<div class="card-header">Actions</div>\n<div class="card-body">\n  <div class="card-text">\n    <a href="/2/update_event/') + ___431) + Cell('">Update</a>\n  </div>\n</div>')))
        html.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___430, adopt=__stack__.all()).inputs, [], [], auto=True)
        html.add_inputs(__stack__.all())
        html.add_inputs(___430.inputs)
    html = (html + Cell('\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/events">Back to events</a>\n</div>'))
    html.add_inputs(__stack__.all())
    try:
        ___432 = make_page(html)[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___432, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/event/<int:ev>')
def _event(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('event', 'ev', ev)
    (__r__, __s__, __a__, __u__) = event(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_event_category(ev, cat):
    global __stack__
    try:
        ___433 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        raise __stop__
    ___434 = ___433
    if ___434:
        __stack__.push()
        __stack__.add(___434.inputs)
        try:
            ___435 = meetup.sql(Cell('INSERT INTO ev_cat (event, category) VALUES (?0, ?1)'), Cell([ev, cat]), stack=__stack__, assigned=['ev_cat'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___435.inputs, bot=True)
        try:
            ___436 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___436, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___434, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True, u=meetup.me())
        __stack__.add(___434.inputs, bot=True)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___434.inputs)
    if non(___434):
        __stack__.push()
        __stack__.add(___434.inputs)
        try:
            ___437 = error_html(Cell('Illegal operation: Add event category'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___438 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___437 + ___438), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___434, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True, u=meetup.me())
        __stack__.add(___434.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/add_event_category/<int:ev>/<int:cat>')
def _add_event_category(ev, cat):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('add_event_category', 'ev', ev)
    cat = meetup.register('add_event_category', 'cat', cat)
    (__r__, __s__, __a__, __u__) = add_event_category(ev, cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_event_category(ev, cat):
    global __stack__
    try:
        ___439 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        raise __stop__
    ___440 = ___439
    if ___440:
        __stack__.push()
        __stack__.add(___440.inputs)
        try:
            ___441 = meetup.sql(Cell('DELETE FROM ev_cat WHERE event = ?0 AND category = ?1'), Cell([ev, cat]), stack=__stack__, assigned=['ev_cat'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___441.inputs, bot=True)
        try:
            ___442 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___442, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___440, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True, u=meetup.me())
        __stack__.add(___440.inputs, bot=True)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___440.inputs)
    if non(___440):
        __stack__.push()
        __stack__.add(___440.inputs)
        try:
            ___443 = error_html(Cell('Illegal operation: Delete event category'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___444 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___443 + ___444), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___440, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True, u=meetup.me())
        __stack__.add(___440.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/delete_event_category/<int:ev>/<int:cat>')
def _delete_event_category(ev, cat):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('delete_event_category', 'ev', ev)
    cat = meetup.register('delete_event_category', 'cat', cat)
    (__r__, __s__, __a__, __u__) = delete_event_category(ev, cat)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_event(ev):
    global __stack__
    try:
        ___445 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___446 = ___445
    if ___446:
        __stack__.push()
        __stack__.add(___446.inputs)
        try:
            ___447 = meetup.sql(Cell('DELETE FROM events WHERE id = ?0'), Cell([ev]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'events', 'ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('requests', __stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___447.inputs, bot=True)
        try:
            ___448 = meetup.sql(Cell('DELETE FROM ev_att WHERE event = ?0'), Cell([ev]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('requests', __stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___448.inputs, bot=True)
        try:
            ___449 = meetup.sql(Cell('DELETE FROM ev_cat WHERE event = ?0'), Cell([ev]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('requests', __stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___449.inputs, bot=True)
        try:
            ___450 = meetup.sql(Cell('DELETE FROM invitations WHERE event = ?0'), Cell([ev]), stack=__stack__, assigned=['requests', 'invitations'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('requests', __stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___450.inputs, bot=True)
        try:
            ___451 = meetup.sql(Cell('DELETE FROM requests WHERE event = ?0'), Cell([ev]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('requests', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___451.inputs, bot=True)
        try:
            ___452 = events()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___452, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___446, adopt=__stack__.all()).inputs, ['ev_cat', 'requests', 'invitations', 'events', 'ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___446.inputs, bot=True)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___446.inputs)
        meetup.add_sql_inputs('requests', __stack__.all())
        meetup.add_sql_inputs('requests', ___446.inputs)
        meetup.add_sql_inputs('invitations', __stack__.all())
        meetup.add_sql_inputs('invitations', ___446.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___446.inputs)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___446.inputs)
    if non(___446):
        __stack__.push()
        __stack__.add(___446.inputs)
        try:
            ___453 = error_html(Cell('Illegal operation: Delete event'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___454 = events()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___453 + ___454), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___446, adopt=__stack__.all()).inputs, ['ev_cat', 'requests', 'invitations', 'events', 'ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___446.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/delete_event/<int:ev>')
def _delete_event(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('delete_event', 'ev', ev)
    (__r__, __s__, __a__, __u__) = delete_event(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_event(ev):
    global __stack__
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('evt' not in locals()):
        evt = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('date' not in locals()):
        date = Cell(None)
    if ('description' not in locals()):
        description = Cell(None)
    if ('time' not in locals()):
        time = Cell(None)
    ___455 = meetup.sql(Cell('SELECT * FROM events WHERE id = ?0'), Cell([ev]))
    evt = ___455[Cell(0)]
    evt.add_inputs(__stack__.all())
    title = evt[Cell(1)]
    title.add_inputs(__stack__.all())
    description = evt[Cell(2)]
    description.add_inputs(__stack__.all())
    ___456 = Cell((evt[Cell(3)] > Cell(0)))
    if ___456:
        __stack__.push()
        __stack__.add(___456.inputs)
        try:
            ___457 = location_html(evt[Cell(3)])[0]
        except Stop as __stop__:
            date.add_inputs(__stop__.inputs)
            time.add_inputs(__stop__.inputs)
            location.add_inputs(__stop__.inputs)
            owner.add_inputs(__stop__.inputs)
            raise __stop__
        location = ___457
        location.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___456, adopt=__stack__.all()).inputs, [], [], auto=True)
        location.add_inputs(__stack__.all())
        location.add_inputs(___456.inputs)
    if non(___456):
        __stack__.push()
        __stack__.add(___456.inputs)
        location = Cell('')
        location.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___456, adopt=__stack__.all()).inputs, [], [], auto=True)
        location.add_inputs(__stack__.all())
        location.add_inputs(___456.inputs)
    time = evt[Cell(4)]
    time.add_inputs(__stack__.all())
    date = evt[Cell(5)]
    date.add_inputs(__stack__.all())
    ___458 = db_str(evt[Cell(6)])
    owner = ___458
    owner.add_inputs(__stack__.all())
    try:
        ___459 = location_select(evt[Cell(3)])[0]
    except Stop as __stop__:
        raise __stop__
    ___460 = db_str(ev)
    ___461 = db_str(ev)
    try:
        ___462 = make_page(((((((((((((((((Cell('<h5 class="card-header">Update event</h5>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/update_event_do">\n      <div class="form-group mb-1">\n        <label for="title" class="form-label">Title</label>\n        <input type="text" name="title" id="title" value="') + title) + Cell('" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="description" class="form-label">Description</label>\n        <input type="text" name="description" id="description" value="')) + description) + Cell('" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="location" class="form-label">Location</label>\n        ')) + ___459) + Cell('\n      </div>\n      <div class="form-group mb-1">\n        <label for="time" class="form-label">Time</label>\n        <input type="text" name="time" id="time" value="')) + time) + Cell('" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="time" class="form-label">Date</label>\n        <input type="text" name="date" id="date" value="')) + date) + Cell('" class="form-control">\n      </div>\n      <input type="hidden" name="owner" id="owner" value=')) + owner) + Cell('>\n      <input type="hidden" name="id_" id="id_" value=')) + ___460) + Cell('>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/event/')) + ___461) + Cell('">Back to event</a>\n</div>')))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___462, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/update_event/<int:ev>')
def _update_event(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('update_event', 'ev', ev)
    (__r__, __s__, __a__, __u__) = update_event(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_event_do():
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('requests' not in locals()):
        requests = Cell(None)
    if ('ev_cat' not in locals()):
        ev_cat = Cell(None)
    if ('request' not in locals()):
        request = Cell(None)
    if ('ev_cats' not in locals()):
        ev_cats = Cell(None)
    if ('title' not in locals()):
        title = Cell(None)
    if ('invitations' not in locals()):
        invitations = Cell(None)
    if ('description' not in locals()):
        description = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('ev_att' not in locals()):
        ev_att = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    if ('new_id' not in locals()):
        new_id = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('ev_atts' not in locals()):
        ev_atts = Cell(None)
    if ('date' not in locals()):
        date = Cell(None)
    if ('invitation' not in locals()):
        invitation = Cell(None)
    if ('time' not in locals()):
        time = Cell(None)
    ___463 = meetup.get('update_event_do', Cell('id_'))
    ___464 = db_int(___463)
    id_ = ___464
    id_.add_inputs(__stack__.all())
    try:
        ___465 = is_manager(id_)[0]
    except Stop as __stop__:
        new_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        ev_atts.add_inputs(__stop__.inputs)
        description.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        location.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        ev_cats.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        invitations.add_inputs(__stop__.inputs)
        time.add_inputs(__stop__.inputs)
        requests.add_inputs(__stop__.inputs)
        date.add_inputs(__stop__.inputs)
        title.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        owner.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('requests', __stop__.inputs)
        ev_att.add_inputs(__stop__.inputs)
        ev_cat.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        invitation.add_inputs(__stop__.inputs)
        request.add_inputs(__stop__.inputs)
        raise __stop__
    try:
        ___466 = is_moderator(id_)[0]
    except Stop as __stop__:
        new_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_cat', __stop__.inputs)
        ev_atts.add_inputs(__stop__.inputs)
        description.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('events', __stop__.inputs)
        location.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        ev_cats.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        invitations.add_inputs(__stop__.inputs)
        time.add_inputs(__stop__.inputs)
        requests.add_inputs(__stop__.inputs)
        date.add_inputs(__stop__.inputs)
        title.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        owner.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('requests', __stop__.inputs)
        ev_att.add_inputs(__stop__.inputs)
        ev_cat.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        invitation.add_inputs(__stop__.inputs)
        request.add_inputs(__stop__.inputs)
        raise __stop__
    ___467 = non(Cell((___465.value or ___466.value), inputs=dict(___465.inputs)))
    if ___467:
        __stack__.push()
        __stack__.add(___467.inputs)
        try:
            ___468 = error_html(Cell('Illegal operation: Update event'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___469 = event(id_)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___468 + ___469), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___467, adopt=__stack__.all()).inputs, ['ev_cat', 'events', 'ev_att', 'requests', 'invitations'], [], auto=True, u=meetup.me())
        __stack__.add(___467.inputs, bot=True)
    if non(___467):
        __stack__.push()
        __stack__.add(___467.inputs)
        ___470 = meetup.get('update_event_do', Cell('title'))
        title = ___470
        title.add_inputs(__stack__.all())
        ___471 = meetup.get('update_event_do', Cell('description'))
        description = ___471
        description.add_inputs(__stack__.all())
        ___472 = meetup.get('update_event_do', Cell('location'))
        ___473 = db_int(___472)
        location = ___473
        location.add_inputs(__stack__.all())
        ___474 = meetup.get('update_event_do', Cell('time'))
        time = ___474
        time.add_inputs(__stack__.all())
        ___475 = meetup.get('update_event_do', Cell('date'))
        date = ___475
        date.add_inputs(__stack__.all())
        ___476 = meetup.get('update_event_do', Cell('owner'))
        ___477 = db_int(___476)
        owner = ___477
        owner.add_inputs(__stack__.all())
        try:
            ___478 = meetup.sql(Cell('DELETE FROM events WHERE id = ?0'), Cell([id_]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'ev_att', 'events'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('requests', __stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            new_id.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            invitations.add_inputs(__stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            ev_att.add_inputs(__stop__.inputs)
            ev_atts.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            requests.add_inputs(__stop__.inputs)
            invitation.add_inputs(__stop__.inputs)
            request.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___478.inputs, bot=True)
        try:
            ___479 = meetup.sql(Cell('INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)'), Cell([title, description, location, time, date, owner]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'ev_att', 'events'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_cat', __stop__.inputs)
            meetup.add_sql_inputs('requests', __stop__.inputs)
            ev_cats.add_inputs(__stop__.inputs)
            new_id.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            invitations.add_inputs(__stop__.inputs)
            ev_cat.add_inputs(__stop__.inputs)
            ev_att.add_inputs(__stop__.inputs)
            ev_atts.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            requests.add_inputs(__stop__.inputs)
            invitation.add_inputs(__stop__.inputs)
            request.add_inputs(__stop__.inputs)
            L.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___479.inputs, bot=True)
        new_id = ___479[Cell(0)]
        new_id.add_inputs(__stack__.all())
        ___480 = meetup.sql(Cell('SELECT * FROM ev_att WHERE event = ?0'), Cell([id_]))
        ev_atts = ___480
        ev_atts.add_inputs(__stack__.all())
        ___481 = db_len(ev_atts)
        L = ___481
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___482 = Cell((i < L))
        while ___482:
            __stack__.push()
            __stack__.add(___482.inputs)
            ev_att = ev_atts[i]
            ev_att.add_inputs(__stack__.all())
            try:
                ___483 = meetup.sql(Cell('DELETE FROM ev_att WHERE id = ?0'), Cell([ev_att[Cell(0)]]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'ev_att'], called=[meetup.me()])
            except Stop as __stop__:
                meetup.add_sql_inputs('ev_cat', __stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                ev_cats.add_inputs(__stop__.inputs)
                ev_att.add_inputs(__stop__.inputs)
                invitations.add_inputs(__stop__.inputs)
                ev_cat.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('ev_att', __stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___483.inputs, bot=True)
            try:
                ___484 = meetup.sql(Cell('INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, ?2)'), Cell([new_id, ev_att[Cell(2)], ev_att[Cell(3)]]), stack=__stack__, assigned=['ev_cat', 'requests', 'invitations', 'ev_att'], called=[meetup.me()])
            except Stop as __stop__:
                meetup.add_sql_inputs('ev_cat', __stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                ev_cats.add_inputs(__stop__.inputs)
                ev_att.add_inputs(__stop__.inputs)
                invitations.add_inputs(__stop__.inputs)
                ev_cat.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('ev_att', __stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___484.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___482 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___482, adopt=__stack__.all()).inputs, ['ev_att'], [], auto=True)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___482.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___482.inputs)
        ev_att.add_inputs(__stack__.all())
        ev_att.add_inputs(___482.inputs)
        ___485 = meetup.sql(Cell('SELECT * FROM ev_cat WHERE event = ?0'), Cell([id_]))
        ev_cats = ___485
        ev_cats.add_inputs(__stack__.all())
        ___486 = db_len(ev_cats)
        L = ___486
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___487 = Cell((i < L))
        while ___487:
            __stack__.push()
            __stack__.add(___487.inputs)
            ev_cat = ev_cats[i]
            ev_cat.add_inputs(__stack__.all())
            try:
                ___488 = meetup.sql(Cell('DELETE FROM ev_cat WHERE id = ?0'), Cell([ev_cat[Cell(0)]]), stack=__stack__, assigned=['requests', 'ev_cat', 'invitations'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                meetup.add_sql_inputs('ev_cat', __stop__.inputs)
                invitations.add_inputs(__stop__.inputs)
                ev_cat.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___488.inputs, bot=True)
            try:
                ___489 = meetup.sql(Cell('INSERT INTO ev_cat (event, category) VALUES (?0, ?1)'), Cell([new_id, ev_cat[Cell(2)]]), stack=__stack__, assigned=['requests', 'ev_cat', 'invitations'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                meetup.add_sql_inputs('ev_cat', __stop__.inputs)
                invitations.add_inputs(__stop__.inputs)
                ev_cat.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___489.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___487 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___487, adopt=__stack__.all()).inputs, ['ev_cat'], [], auto=True)
        ev_cat.add_inputs(__stack__.all())
        ev_cat.add_inputs(___487.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___487.inputs)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___487.inputs)
        ___490 = meetup.sql(Cell('SELECT * FROM invitations WHERE event = ?0'), Cell([id_]))
        invitations = ___490
        invitations.add_inputs(__stack__.all())
        ___491 = db_len(invitations)
        L = ___491
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___492 = Cell((i < L))
        while ___492:
            __stack__.push()
            __stack__.add(___492.inputs)
            invitation = invitations[i]
            invitation.add_inputs(__stack__.all())
            try:
                ___493 = meetup.sql(Cell('DELETE FROM invitations WHERE id = ?0'), Cell([invitation[Cell(0)]]), stack=__stack__, assigned=['requests', 'invitations'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___493.inputs, bot=True)
            try:
                ___494 = meetup.sql(Cell('INSERT INTO invitations (inviter, invitee, event) VALUES (?0, ?1, ?2)'), Cell([invitation[Cell(1)], invitation[Cell(2)], new_id]), stack=__stack__, assigned=['requests', 'invitations'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                meetup.add_sql_inputs('invitations', __stop__.inputs)
                requests.add_inputs(__stop__.inputs)
                invitation.add_inputs(__stop__.inputs)
                request.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___494.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___492 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___492, adopt=__stack__.all()).inputs, ['invitations'], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___492.inputs)
        meetup.add_sql_inputs('invitations', __stack__.all())
        meetup.add_sql_inputs('invitations', ___492.inputs)
        invitation.add_inputs(__stack__.all())
        invitation.add_inputs(___492.inputs)
        ___495 = meetup.sql(Cell('SELECT * FROM requests WHERE event = ?0'), Cell([id_]))
        requests = ___495
        requests.add_inputs(__stack__.all())
        ___496 = db_len(requests)
        L = ___496
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___497 = Cell((i < L))
        while ___497:
            __stack__.push()
            __stack__.add(___497.inputs)
            request = requests[i]
            request.add_inputs(__stack__.all())
            try:
                ___498 = meetup.sql(Cell('DELETE FROM requests WHERE id = ?0'), Cell([request[Cell(0)]]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                request.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___498.inputs, bot=True)
            try:
                ___499 = meetup.sql(Cell('INSERT INTO requests (requester, event) VALUES (?0, ?1)'), Cell([request[Cell(1)], new_id]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('requests', __stop__.inputs)
                request.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___499.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___497 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___497, adopt=__stack__.all()).inputs, ['requests'], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___497.inputs)
        meetup.add_sql_inputs('requests', __stack__.all())
        meetup.add_sql_inputs('requests', ___497.inputs)
        request.add_inputs(__stack__.all())
        request.add_inputs(___497.inputs)
        try:
            ___500 = event(new_id)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___500, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___467, adopt=__stack__.all()).inputs, ['ev_cat', 'events', 'ev_att', 'requests', 'invitations'], [], auto=True, u=meetup.me())
        __stack__.add(___467.inputs, bot=True)
        new_id.add_inputs(__stack__.all())
        new_id.add_inputs(___467.inputs)
        meetup.add_sql_inputs('ev_cat', __stack__.all())
        meetup.add_sql_inputs('ev_cat', ___467.inputs)
        ev_atts.add_inputs(__stack__.all())
        ev_atts.add_inputs(___467.inputs)
        description.add_inputs(__stack__.all())
        description.add_inputs(___467.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___467.inputs)
        location.add_inputs(__stack__.all())
        location.add_inputs(___467.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___467.inputs)
        ev_cats.add_inputs(__stack__.all())
        ev_cats.add_inputs(___467.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___467.inputs)
        invitations.add_inputs(__stack__.all())
        invitations.add_inputs(___467.inputs)
        time.add_inputs(__stack__.all())
        time.add_inputs(___467.inputs)
        requests.add_inputs(__stack__.all())
        requests.add_inputs(___467.inputs)
        date.add_inputs(__stack__.all())
        date.add_inputs(___467.inputs)
        title.add_inputs(__stack__.all())
        title.add_inputs(___467.inputs)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___467.inputs)
        owner.add_inputs(__stack__.all())
        owner.add_inputs(___467.inputs)
        meetup.add_sql_inputs('requests', __stack__.all())
        meetup.add_sql_inputs('requests', ___467.inputs)
        ev_att.add_inputs(__stack__.all())
        ev_att.add_inputs(___467.inputs)
        ev_cat.add_inputs(__stack__.all())
        ev_cat.add_inputs(___467.inputs)
        meetup.add_sql_inputs('invitations', __stack__.all())
        meetup.add_sql_inputs('invitations', ___467.inputs)
        invitation.add_inputs(__stack__.all())
        invitation.add_inputs(___467.inputs)
        request.add_inputs(__stack__.all())
        request.add_inputs(___467.inputs)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/update_event_do')
def _update_event_do():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = update_event_do()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def promote_attendee(ev, att):
    global __stack__
    if ('evt' not in locals()):
        evt = Cell(None)
    try:
        ___501 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___502 = meetup.me()
    try:
        ___503 = is_premium()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___504 = Cell((___501.value or Cell((Cell((evt[Cell(6)] == ___502)).value and ___503.value), inputs=dict(Cell((evt[Cell(6)] == ___502)).inputs)).value), inputs=dict(___501.inputs))
    if ___504:
        __stack__.push()
        __stack__.add(___504.inputs)
        try:
            ___505 = meetup.sql(Cell('DELETE FROM ev_att WHERE event = ?0 AND attendee = ?1'), Cell([ev, att]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___505.inputs, bot=True)
        try:
            ___506 = meetup.sql(Cell('INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 2)'), Cell([ev, att]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___506.inputs, bot=True)
        try:
            ___507 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___507, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___504, adopt=__stack__.all()).inputs, ['ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___504.inputs, bot=True)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___504.inputs)
    if non(___504):
        __stack__.push()
        __stack__.add(___504.inputs)
        try:
            ___508 = error_html(Cell('Illegal operation: Promote attendee'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___509 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___508 + ___509), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___504, adopt=__stack__.all()).inputs, ['ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___504.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/promote_attendee/<int:ev>/<int:att>')
def _promote_attendee(ev, att):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('promote_attendee', 'ev', ev)
    att = meetup.register('promote_attendee', 'att', att)
    (__r__, __s__, __a__, __u__) = promote_attendee(ev, att)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def revoke_moderator(ev, att):
    global __stack__
    if ('evt' not in locals()):
        evt = Cell(None)
    try:
        ___510 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___511 = meetup.me()
    try:
        ___512 = is_premium()[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___513 = Cell((___510.value or Cell((Cell((evt[Cell(6)] == ___511)).value and ___512.value), inputs=dict(Cell((evt[Cell(6)] == ___511)).inputs)).value), inputs=dict(___510.inputs))
    if ___513:
        __stack__.push()
        __stack__.add(___513.inputs)
        try:
            ___514 = meetup.sql(Cell('DELETE FROM ev_att WHERE event = ?0 AND attendee = ?1'), Cell([ev, att]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___514.inputs, bot=True)
        try:
            ___515 = meetup.sql(Cell('INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)'), Cell([ev, att]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___515.inputs, bot=True)
        try:
            ___516 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___516, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___513, adopt=__stack__.all()).inputs, ['ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___513.inputs, bot=True)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___513.inputs)
    if non(___513):
        __stack__.push()
        __stack__.add(___513.inputs)
        try:
            ___517 = error_html(Cell('Illegal operation: Revoke moderator'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___518 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___517 + ___518), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___513, adopt=__stack__.all()).inputs, ['ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___513.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/revoke_moderator/<int:ev>/<int:att>')
def _revoke_moderator(ev, att):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('revoke_moderator', 'ev', ev)
    att = meetup.register('revoke_moderator', 'att', att)
    (__r__, __s__, __a__, __u__) = revoke_moderator(ev, att)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def accept_request(ev, req):
    global __stack__
    try:
        ___519 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        meetup.add_sql_inputs('ev_att', __stop__.inputs)
        raise __stop__
    ___520 = ___519
    if ___520:
        __stack__.push()
        __stack__.add(___520.inputs)
        try:
            ___521 = meetup.sql(Cell('DELETE FROM requests WHERE event = ?0 AND requester = ?1'), Cell([ev, req]), stack=__stack__, assigned=['requests', 'ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('requests', __stop__.inputs)
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___521.inputs, bot=True)
        try:
            ___522 = meetup.sql(Cell('INSERT INTO ev_att (event, attendee, level) VALUES (?0, ?1, 1)'), Cell([ev, req]), stack=__stack__, assigned=['ev_att'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('ev_att', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___522.inputs, bot=True)
        try:
            ___523 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___523, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___520, adopt=__stack__.all()).inputs, ['requests', 'ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___520.inputs, bot=True)
        meetup.add_sql_inputs('requests', __stack__.all())
        meetup.add_sql_inputs('requests', ___520.inputs)
        meetup.add_sql_inputs('ev_att', __stack__.all())
        meetup.add_sql_inputs('ev_att', ___520.inputs)
    if non(___520):
        __stack__.push()
        __stack__.add(___520.inputs)
        try:
            ___524 = error_html(Cell('Illegal operation: Accept request'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___525 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___524 + ___525), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___520, adopt=__stack__.all()).inputs, ['requests', 'ev_att'], [], auto=True, u=meetup.me())
        __stack__.add(___520.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/accept_request/<int:ev>/<int:req>')
def _accept_request(ev, req):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('accept_request', 'ev', ev)
    req = meetup.register('accept_request', 'req', req)
    (__r__, __s__, __a__, __u__) = accept_request(ev, req)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def reject_request(ev, req):
    global __stack__
    try:
        ___526 = is_manager(ev)[0]
    except Stop as __stop__:
        meetup.add_sql_inputs('requests', __stop__.inputs)
        raise __stop__
    ___527 = ___526
    if ___527:
        __stack__.push()
        __stack__.add(___527.inputs)
        try:
            ___528 = meetup.sql(Cell('DELETE FROM requests WHERE event = ?0 AND requester = ?1'), Cell([ev, req]), stack=__stack__, assigned=['requests'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('requests', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___528.inputs, bot=True)
        try:
            ___529 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___529, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___527, adopt=__stack__.all()).inputs, ['requests'], [], auto=True, u=meetup.me())
        __stack__.add(___527.inputs, bot=True)
        meetup.add_sql_inputs('requests', __stack__.all())
        meetup.add_sql_inputs('requests', ___527.inputs)
    if non(___527):
        __stack__.push()
        __stack__.add(___527.inputs)
        try:
            ___530 = error_html(Cell('Illegal operation: Reject request'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___531 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___530 + ___531), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___527, adopt=__stack__.all()).inputs, ['requests'], [], auto=True, u=meetup.me())
        __stack__.add(___527.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/reject_request/<int:ev>/<int:req>')
def _reject_request(ev, req):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('reject_request', 'ev', ev)
    req = meetup.register('reject_request', 'req', req)
    (__r__, __s__, __a__, __u__) = reject_request(ev, req)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def invite(ev):
    global __stack__
    if ('user_id' not in locals()):
        user_id = Cell(None)
    try:
        ___532 = is_manager(ev)[0]
    except Stop as __stop__:
        user_id.add_inputs(__stop__.inputs)
        meetup.add_sql_inputs('invitations', __stop__.inputs)
        raise __stop__
    ___533 = ___532
    if ___533:
        __stack__.push()
        __stack__.add(___533.inputs)
        ___534 = meetup.get('invite', Cell('ID'))
        user_id = ___534
        user_id.add_inputs(__stack__.all())
        ___535 = meetup.me()
        try:
            ___536 = meetup.sql(Cell('INSERT INTO invitations (inviter, invitee, event) VALUES (?0, ?1, ?2)'), Cell([___535, user_id, ev]), stack=__stack__, assigned=['invitations'], called=[meetup.me()])
        except Stop as __stop__:
            meetup.add_sql_inputs('invitations', __stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___536.inputs, bot=True)
        try:
            ___537 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___537, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___533, adopt=__stack__.all()).inputs, ['invitations'], [], auto=True, u=meetup.me())
        __stack__.add(___533.inputs, bot=True)
        user_id.add_inputs(__stack__.all())
        user_id.add_inputs(___533.inputs)
        meetup.add_sql_inputs('invitations', __stack__.all())
        meetup.add_sql_inputs('invitations', ___533.inputs)
    if non(___533):
        __stack__.push()
        __stack__.add(___533.inputs)
        try:
            ___538 = error_html(Cell('Illegal operation: Invite'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___539 = event(ev)[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___538 + ___539), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___533, adopt=__stack__.all()).inputs, ['invitations'], [], auto=True, u=meetup.me())
        __stack__.add(___533.inputs, bot=True)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/invite/<int:ev>')
def _invite(ev):
    global __stack__
    __stack__ = Stack()
    ev = meetup.register('invite', 'ev', ev)
    (__r__, __s__, __a__, __u__) = invite(ev)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def locations():
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('table' not in locals()):
        table = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('footer' not in locals()):
        footer = Cell(None)
    if ('locs' not in locals()):
        locs = Cell(None)
    if ('header' not in locals()):
        header = Cell(None)
    if ('location' not in locals()):
        location = Cell(None)
    header = Cell('<h5 class="card-header">Locations</h5>\n<div class="card-body">\n  <div class="card-text">\n    <table class="table">\n      <thead>\n        <tr><th>Country</th><th>Name</th><th>Actions</th></tr>\n      </thead>\n      <tbody>\n')
    header.add_inputs(__stack__.all())
    table = Cell('')
    table.add_inputs(__stack__.all())
    try:
        ___540 = is_admin()[0]
    except Stop as __stop__:
        location.add_inputs(__stop__.inputs)
        table.add_inputs(__stop__.inputs)
        L.add_inputs(__stop__.inputs)
        footer.add_inputs(__stop__.inputs)
        i.add_inputs(__stop__.inputs)
        locs.add_inputs(__stop__.inputs)
        raise __stop__
    ___541 = ___540
    if ___541:
        __stack__.push()
        __stack__.add(___541.inputs)
        footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>\n<div class="card-header">Add new location</div>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/add_location">\n      <div class="form-group mb-1">\n        <label for="country" class="form-label">Country</label>\n        <input type="text" name="country" id="country" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="name" class="form-label">Name</label>\n        <input type="text" name="name" id="name" class="form-control">\n      </div>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n')
        footer.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___541, adopt=__stack__.all()).inputs, [], [], auto=True)
        footer.add_inputs(__stack__.all())
        footer.add_inputs(___541.inputs)
    if non(___541):
        __stack__.push()
        __stack__.add(___541.inputs)
        footer = Cell('\n      </tbody>\n    </table>\n  </div>\n</div>')
        footer.add_inputs(__stack__.all())
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___541, adopt=__stack__.all()).inputs, [], [], auto=True)
        footer.add_inputs(__stack__.all())
        footer.add_inputs(___541.inputs)
    ___542 = meetup.me()
    ___543 = meetup.sql(Cell('SELECT locations.* FROM friends LEFT JOIN locations ON friends.friend_id = locations.owner WHERE friends.user_id = ?0 OR locations.owner = ?0'), Cell([___542]))
    locs = ___543
    locs.add_inputs(__stack__.all())
    ___544 = db_len(locs)
    L = ___544
    L.add_inputs(__stack__.all())
    i = Cell(0)
    i.add_inputs(__stack__.all())
    ___545 = Cell((i < L))
    while ___545:
        __stack__.push()
        __stack__.add(___545.inputs)
        location = locs[i]
        location.add_inputs(__stack__.all())
        ___546 = db_str(location[Cell(1)])
        ___547 = db_str(location[Cell(2)])
        table = (table + ((((Cell('<tr><td>') + ___546) + Cell('</td><td>')) + ___547) + Cell('</td>')))
        table.add_inputs(__stack__.all())
        ___548 = meetup.me()
        ___549 = Cell((location[Cell(3)] == ___548))
        if ___549:
            __stack__.push()
            __stack__.add(___549.inputs)
            ___550 = db_str(location[Cell(0)])
            ___551 = db_str(location[Cell(0)])
            table = (table + ((((Cell('<td><a href="/2/delete_location/') + ___550) + Cell('">Delete</a>&nbsp;<a href="/2/update_location/')) + ___551) + Cell('">Update</a></td></tr>')))
            table.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___549, adopt=__stack__.all()).inputs, [], [], auto=True)
            table.add_inputs(__stack__.all())
            table.add_inputs(___549.inputs)
        if non(___549):
            __stack__.push()
            __stack__.add(___549.inputs)
            table = (table + Cell('<td></td></tr>'))
            table.add_inputs(__stack__.all())
            __stack__.pop()
        else:
            logsanitize(meetup.id_, Cell(___549, adopt=__stack__.all()).inputs, [], [], auto=True)
            table.add_inputs(__stack__.all())
            table.add_inputs(___549.inputs)
        i = (i + Cell(1))
        i.add_inputs(__stack__.all())
        __stack__.pop()
        ___545 = Cell((i < L))
    logsanitize(meetup.id_, Cell(___545, adopt=__stack__.all()).inputs, [], [], auto=True)
    location.add_inputs(__stack__.all())
    location.add_inputs(___545.inputs)
    table.add_inputs(__stack__.all())
    table.add_inputs(___545.inputs)
    i.add_inputs(__stack__.all())
    i.add_inputs(___545.inputs)
    try:
        ___552 = make_page(((header + table) + footer))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___552, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/locations')
def _locations():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = locations()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def delete_location(location):
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('evs' not in locals()):
        evs = Cell(None)
    if ('usrs' not in locals()):
        usrs = Cell(None)
    if ('ev' not in locals()):
        ev = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('usr' not in locals()):
        usr = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    ___553 = meetup.sql(Cell('SELECT owner FROM locations WHERE id = ?0'), Cell([location]))
    owner = ___553[Cell(0)][Cell(0)]
    owner.add_inputs(__stack__.all())
    ___554 = meetup.me()
    ___555 = Cell((owner != ___554))
    if ___555:
        __stack__.push()
        __stack__.add(___555.inputs)
        try:
            ___556 = error_html(Cell('Illegal operation: Delete location'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___557 = locations()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___556 + ___557), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___555, adopt=__stack__.all()).inputs, ['locations', 'users', 'events'], [], auto=True, u=meetup.me())
        __stack__.add(___555.inputs, bot=True)
    if non(___555):
        __stack__.push()
        __stack__.add(___555.inputs)
        try:
            ___558 = meetup.sql(Cell('DELETE FROM locations WHERE id = ?0'), Cell([location]), stack=__stack__, assigned=['locations', 'users', 'events'], called=[meetup.me()])
        except Stop as __stop__:
            evs.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('locations', __stop__.inputs)
            usr.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('users', __stop__.inputs)
            ev.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            usrs.add_inputs(__stop__.inputs)
            i.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___558.inputs, bot=True)
        ___559 = meetup.sql(Cell('SELECT * FROM events WHERE location = ?0'), Cell([id_]))
        evs = ___559
        evs.add_inputs(__stack__.all())
        ___560 = db_len(evs)
        L = ___560
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___561 = Cell((i < L))
        while ___561:
            __stack__.push()
            __stack__.add(___561.inputs)
            ev = evs[i]
            ev.add_inputs(__stack__.all())
            try:
                ___562 = meetup.sql(Cell('DELETE FROM events WHERE id = ?0'), Cell([ev[Cell(0)]]), stack=__stack__, assigned=['users', 'events'], called=[meetup.me()])
            except Stop as __stop__:
                usr.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                L.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                ev.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('events', __stop__.inputs)
                usrs.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___562.inputs, bot=True)
            try:
                ___563 = meetup.sql(Cell('INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)'), Cell([ev[Cell(1)], ev[Cell(2)], Cell(0), ev[Cell(3)], ev[Cell(4)], ev[Cell(5)]]), stack=__stack__, assigned=['users', 'events'], called=[meetup.me()])
            except Stop as __stop__:
                usr.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                L.add_inputs(__stop__.inputs)
                i.add_inputs(__stop__.inputs)
                ev.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('events', __stop__.inputs)
                usrs.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___563.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___561 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___561, adopt=__stack__.all()).inputs, ['events'], [], auto=True)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___561.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___561.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___561.inputs)
        ___564 = meetup.sql(Cell('SELECT * FROM users WHERE address = ?0'), Cell([id_]))
        usrs = ___564
        usrs.add_inputs(__stack__.all())
        ___565 = db_len(usrs)
        L = ___565
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___566 = Cell((i < L))
        while ___566:
            __stack__.push()
            __stack__.add(___566.inputs)
            usr = usrs[i]
            usr.add_inputs(__stack__.all())
            try:
                ___567 = meetup.sql(Cell('DELETE FROM users WHERE id = ?0'), Cell([usr[Cell(0)]]), stack=__stack__, assigned=['users'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___567.inputs, bot=True)
            try:
                ___568 = meetup.sql(Cell('INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)'), Cell([usr[Cell(1)], usr[Cell(2)], usr[Cell(3)], Cell(0)]), stack=__stack__, assigned=['users'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___568.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___566 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___566, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___566.inputs)
        usr.add_inputs(__stack__.all())
        usr.add_inputs(___566.inputs)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___566.inputs)
        try:
            ___569 = locations()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___569, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___555, adopt=__stack__.all()).inputs, ['locations', 'users', 'events'], [], auto=True, u=meetup.me())
        __stack__.add(___555.inputs, bot=True)
        evs.add_inputs(__stack__.all())
        evs.add_inputs(___555.inputs)
        meetup.add_sql_inputs('locations', __stack__.all())
        meetup.add_sql_inputs('locations', ___555.inputs)
        usr.add_inputs(__stack__.all())
        usr.add_inputs(___555.inputs)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___555.inputs)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___555.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___555.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___555.inputs)
        usrs.add_inputs(__stack__.all())
        usrs.add_inputs(___555.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___555.inputs)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/delete_location/<int:location>')
def _delete_location(location):
    global __stack__
    __stack__ = Stack()
    location = meetup.register('delete_location', 'location', location)
    (__r__, __s__, __a__, __u__) = delete_location(location)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def add_location():
    global __stack__
    if ('name' not in locals()):
        name = Cell(None)
    if ('country' not in locals()):
        country = Cell(None)
    ___570 = meetup.get('add_location', Cell('country'))
    country = ___570
    country.add_inputs(__stack__.all())
    ___571 = meetup.get('add_location', Cell('name'))
    name = ___571
    name.add_inputs(__stack__.all())
    ___572 = meetup.me()
    try:
        ___573 = meetup.sql(Cell('INSERT INTO locations (country, name, owner) VALUES (?0, ?1, ?2)'), Cell([country, name, ___572]), stack=__stack__, assigned=['locations'], called=[meetup.me()])
    except Stop as __stop__:
        meetup.add_sql_inputs('locations', __stop__.inputs)
        raise __stop__
    else:
        __stack__.add(___573.inputs, bot=True)
    try:
        ___574 = locations()[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___574, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/add_location')
def _add_location():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = add_location()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_location(location):
    global __stack__
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('country' not in locals()):
        country = Cell(None)
    if ('location_' not in locals()):
        location_ = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    ___575 = meetup.sql(Cell('SELECT * FROM locations WHERE id = ?0'), Cell([location]))
    location_ = ___575[Cell(0)]
    location_.add_inputs(__stack__.all())
    ___576 = db_str(location_[Cell(0)])
    id_ = ___576
    id_.add_inputs(__stack__.all())
    country = location_[Cell(1)]
    country.add_inputs(__stack__.all())
    name = location_[Cell(2)]
    name.add_inputs(__stack__.all())
    owner = location_[Cell(3)]
    owner.add_inputs(__stack__.all())
    try:
        ___577 = make_page(((((((((Cell('<h5 class="card-header">Update location</h5>\n<div class="card-body">\n  <div class="card-text">\n    <form action="/2/update_location_do">\n      <input type="hidden" name="id_" id="id_" value="') + id_) + Cell('">\n      <input type="hidden" name="owner" id="owner" value="')) + owner) + Cell('">\n      <div class="form-group mb-1">\n        <label for="country" class="form-label">Country</label>\n        <input type="text" name="country" id="country" value="')) + country) + Cell('" class="form-control">\n      </div>\n      <div class="form-group mb-1">\n        <label for="name" class="form-label">Name</label>\n        <input type="text" name="name" id="name" value="')) + name) + Cell('" class="form-control">\n      </div>\n      <input type="submit" value="Submit" class="btn btn-primary">\n    </form>\n  </div>\n</div>\n<div class="list-group list-group-flush">\n  <a class="list-group-item list-group-item-action list-group-item-dark" href="/2/locations">Back to locations</a>\n</div>\n')))[0]
    except Stop as __stop__:
        raise __stop__
    __r__ = Cell(___577, adopt=__stack__.all())
    __s__ = __stack__.all()
    return (__r__, __s__, [], [])

@meetup.route('/update_location/<int:location>')
def _update_location(location):
    global __stack__
    __stack__ = Stack()
    location = meetup.register('update_location', 'location', location)
    (__r__, __s__, __a__, __u__) = update_location(location)
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__

def update_location_do():
    global __stack__
    if ('L' not in locals()):
        L = Cell(None)
    if ('owner' not in locals()):
        owner = Cell(None)
    if ('evs' not in locals()):
        evs = Cell(None)
    if ('country' not in locals()):
        country = Cell(None)
    if ('name' not in locals()):
        name = Cell(None)
    if ('usrs' not in locals()):
        usrs = Cell(None)
    if ('ev' not in locals()):
        ev = Cell(None)
    if ('i' not in locals()):
        i = Cell(None)
    if ('new_id' not in locals()):
        new_id = Cell(None)
    if ('usr' not in locals()):
        usr = Cell(None)
    if ('id_' not in locals()):
        id_ = Cell(None)
    ___578 = meetup.get('update_location_do', Cell('id_'))
    ___579 = db_int(___578)
    id_ = ___579
    id_.add_inputs(__stack__.all())
    ___580 = meetup.sql(Cell('SELECT owner FROM locations WHERE id = ?0'), Cell([id_]))
    owner = ___580[Cell(0)][Cell(0)]
    owner.add_inputs(__stack__.all())
    ___581 = meetup.me()
    ___582 = Cell((owner != ___581))
    if ___582:
        __stack__.push()
        __stack__.add(___582.inputs)
        try:
            ___583 = error_html(Cell('Illegal operation: Update location'))[0]
        except Stop as __stop__:
            raise __stop__
        try:
            ___584 = locations()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell((___583 + ___584), adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___582, adopt=__stack__.all()).inputs, ['locations', 'users', 'events'], [], auto=True, u=meetup.me())
        __stack__.add(___582.inputs, bot=True)
    if non(___582):
        __stack__.push()
        __stack__.add(___582.inputs)
        ___585 = meetup.get('update_location_do', Cell('country'))
        country = ___585
        country.add_inputs(__stack__.all())
        ___586 = meetup.get('update_location_do', Cell('name'))
        name = ___586
        name.add_inputs(__stack__.all())
        try:
            ___587 = meetup.sql(Cell('DELETE FROM locations WHERE id = ?0'), Cell([id_]), stack=__stack__, assigned=['locations', 'users', 'events'], called=[meetup.me()])
        except Stop as __stop__:
            ev.add_inputs(__stop__.inputs)
            usr.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('locations', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('users', __stop__.inputs)
            i.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            new_id.add_inputs(__stop__.inputs)
            usrs.add_inputs(__stop__.inputs)
            evs.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___587.inputs, bot=True)
        try:
            ___588 = meetup.sql(Cell('INSERT INTO locations (country, name) VALUES (?0, ?1)'), Cell([country, name]), stack=__stack__, assigned=['locations', 'users', 'events'], called=[meetup.me()])
        except Stop as __stop__:
            ev.add_inputs(__stop__.inputs)
            usr.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('locations', __stop__.inputs)
            L.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('users', __stop__.inputs)
            i.add_inputs(__stop__.inputs)
            meetup.add_sql_inputs('events', __stop__.inputs)
            new_id.add_inputs(__stop__.inputs)
            usrs.add_inputs(__stop__.inputs)
            evs.add_inputs(__stop__.inputs)
            raise __stop__
        else:
            __stack__.add(___588.inputs, bot=True)
        new_id = ___588[Cell(0)]
        new_id.add_inputs(__stack__.all())
        ___589 = meetup.sql(Cell('SELECT * FROM events WHERE location = ?0'), Cell([id_]))
        evs = ___589
        evs.add_inputs(__stack__.all())
        ___590 = db_len(evs)
        L = ___590
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___591 = Cell((i < L))
        while ___591:
            __stack__.push()
            __stack__.add(___591.inputs)
            ev = evs[i]
            ev.add_inputs(__stack__.all())
            try:
                ___592 = meetup.sql(Cell('DELETE FROM events WHERE id = ?0'), Cell([ev[Cell(0)]]), stack=__stack__, assigned=['users', 'events'], called=[meetup.me()])
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('events', __stop__.inputs)
                usrs.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___592.inputs, bot=True)
            try:
                ___593 = meetup.sql(Cell('INSERT INTO events (title, description, location, time, date, owner) VALUES (?0, ?1, ?2, ?3, ?4, ?5)'), Cell([ev[Cell(1)], ev[Cell(2)], new_id, ev[Cell(3)], ev[Cell(4)], ev[Cell(5)]]), stack=__stack__, assigned=['users', 'events'], called=[meetup.me()])
            except Stop as __stop__:
                ev.add_inputs(__stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                L.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('events', __stop__.inputs)
                usrs.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___593.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___591 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___591, adopt=__stack__.all()).inputs, ['events'], [], auto=True)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___591.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___591.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___591.inputs)
        ___594 = meetup.sql(Cell('SELECT * FROM users WHERE address = ?0'), Cell([id_]))
        usrs = ___594
        usrs.add_inputs(__stack__.all())
        ___595 = db_len(usrs)
        L = ___595
        L.add_inputs(__stack__.all())
        i = Cell(0)
        i.add_inputs(__stack__.all())
        ___596 = Cell((i < L))
        while ___596:
            __stack__.push()
            __stack__.add(___596.inputs)
            usr = usrs[i]
            usr.add_inputs(__stack__.all())
            try:
                ___597 = meetup.sql(Cell('DELETE FROM users WHERE id = ?0'), Cell([usr[Cell(0)]]), stack=__stack__, assigned=['users'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___597.inputs, bot=True)
            try:
                ___598 = meetup.sql(Cell('INSERT INTO users (user_id, name, level, address) VALUES (?0, ?1, ?2, ?3)'), Cell([usr[Cell(1)], usr[Cell(2)], usr[Cell(3)], new_id]), stack=__stack__, assigned=['users'], called=[meetup.me()])
            except Stop as __stop__:
                i.add_inputs(__stop__.inputs)
                meetup.add_sql_inputs('users', __stop__.inputs)
                usr.add_inputs(__stop__.inputs)
                raise __stop__
            else:
                __stack__.add(___598.inputs, bot=True)
            i = (i + Cell(1))
            i.add_inputs(__stack__.all())
            __stack__.pop()
            ___596 = Cell((i < L))
        logsanitize(meetup.id_, Cell(___596, adopt=__stack__.all()).inputs, ['users'], [], auto=True)
        i.add_inputs(__stack__.all())
        i.add_inputs(___596.inputs)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___596.inputs)
        usr.add_inputs(__stack__.all())
        usr.add_inputs(___596.inputs)
        try:
            ___599 = locations()[0]
        except Stop as __stop__:
            raise __stop__
        __r__ = Cell(___599, adopt=__stack__.all())
        __s__ = __stack__.all()
        __stack__.pop()
        return (__r__, __s__, [], [])
        __stack__.pop()
    else:
        logsanitize(meetup.id_, Cell(___582, adopt=__stack__.all()).inputs, ['locations', 'users', 'events'], [], auto=True, u=meetup.me())
        __stack__.add(___582.inputs, bot=True)
        ev.add_inputs(__stack__.all())
        ev.add_inputs(___582.inputs)
        usr.add_inputs(__stack__.all())
        usr.add_inputs(___582.inputs)
        meetup.add_sql_inputs('locations', __stack__.all())
        meetup.add_sql_inputs('locations', ___582.inputs)
        L.add_inputs(__stack__.all())
        L.add_inputs(___582.inputs)
        meetup.add_sql_inputs('users', __stack__.all())
        meetup.add_sql_inputs('users', ___582.inputs)
        i.add_inputs(__stack__.all())
        i.add_inputs(___582.inputs)
        country.add_inputs(__stack__.all())
        country.add_inputs(___582.inputs)
        meetup.add_sql_inputs('events', __stack__.all())
        meetup.add_sql_inputs('events', ___582.inputs)
        new_id.add_inputs(__stack__.all())
        new_id.add_inputs(___582.inputs)
        usrs.add_inputs(__stack__.all())
        usrs.add_inputs(___582.inputs)
        name.add_inputs(__stack__.all())
        name.add_inputs(___582.inputs)
        evs.add_inputs(__stack__.all())
        evs.add_inputs(___582.inputs)
    __s__ = __stack__.all()
    return (None, __s__, [], [])

@meetup.route('/update_location_do')
def _update_location_do():
    global __stack__
    __stack__ = Stack()
    (__r__, __s__, __a__, __u__) = update_location_do()
    logreturn(meetup.id_, meetup.me(), __r__, __s__, __a__, __u__, auto=True)
    return __r__
