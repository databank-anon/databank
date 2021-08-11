import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Flask, request, session, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing

meetup = Flask(__name__)
meetup.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(meetup)
meetup.secret_key = "E4kB3BUlTXivYtkaKnCb9XHGIr9erSEIX0n0MWOnAqlqr2PGKWjPgWp2834M5PmDqx2dEvI2EV7YdriY"
hashing = Hashing(meetup)

cat_mod = db.Table('cat_mod',
                   db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False))

cat_sub = db.Table('cat_sub',
                   db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False))

ev_cat = db.Table('ev_cat',
                  db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False),
                  db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False))

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscribers = db.relationship('User', secondary=cat_sub, lazy='subquery',
                                  backref=db.backref('subscriptions', lazy=True))
    moderators = db.relationship('User', secondary=cat_mod, lazy='subquery',
                                 backref=db.backref('moderated', lazy=True))
    events = db.relationship('Event', secondary=ev_cat, lazy='subquery',
                             backref=db.backref('categories', lazy=True))

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column('id', db.Integer, primary_key=True)
    country = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, country, owner_id):
        self.name = name
        self.country = country
        self.owner_id = owner_id

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    time = db.Column(db.Text)
    date = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, owner_id, location_id=None, time=None, date=None):
        self.title = title
        self.description = description
        self.owner_id = owner_id
        self.location_id = location_id
        self.time = time
        self.date = date

class Invitation(db.Model):
    __tablename__ = 'invitation'
    id = db.Column('id', db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inviter = db.relationship('User', foreign_keys='Invitation.inviter_id')
    invitee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event')

    def __init__(self, inviter_id, invitee_id, event_id):
        self.inviter_id = inviter_id
        self.invitee_id = invitee_id
        self.event_id = event_id

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column('id', db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requester = db.relationship('User')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    def __init__(self, requester_id, event_id):
        self.requester_id = requester_id
        self.event_id = event_id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    owned_events = db.relationship('Event', backref='user', lazy=True)

class Ev_att(db.Model):
    __tablename__ = 'ev_att'
    id = db.Column('id', db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    attendee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attendee = db.relationship('User')
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, event_id, attendee_id, level):
        self.event_id = event_id
        self.attendee_id = attendee_id
        self.level = level

@meetup.route('/')
def index():
    user_id = session.get('user_id', None)
    user_name = session.get('user_name', None)
    wrong_pass = request.args.get('wrong_pass', None)
    return render_template('index.html', **locals())

def logged_only(f):
    def wrapper(*args, **kwargs):
        if session.get('user_id', None) is None:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def location_html(location):
    location_ = Location.get(location)
    if location_ is None:
        return ""
    else:
        return f"{location.name} ({location.country})"

def error_html(msg):
    return f'<div class="alert alert-danger" role="alert">{{ msg }}</div>'

def me():
    return session['user_id']

def location_select(selected):
    options = "<option value=\"0\"></option>"
    for location in Location.query.all():
        sel = " selected=\"selected\"" if selected == location.id else ""
        options += f"<option value=\"{location.id}\"{sel}>{location.name} ({location.country})"
    return "<select name=\"location\" id=\"location\" class=\"form-select\">" + options + "</select>"
    
def event_html(event, detail=True):
    location = location_html(event.location_id) if event.location_id else ""
    time_date = event.date + " " + event.time
    if detail:
        attended = Ev_att.query.filter_by(event_id=event.id, attendee_id=me()).count()
        if attended > 0:
            leave = f"<tr><td colspan\"2\"><a href=\"/leave_event/{event.id}\">Leave</a></td></tr>"
        else:
            leave = f"<tr><td colspan\"2\"><a href=\"/request_attendance/{event.id}\">Request attendance</a></td></tr>"
        invited = Invitation.query.filter_by(event_id=event.id, invitee_id=me())
        if invited.count() > 0:
            invitation = invited.one().id
            leave += f"<tr><td colspan\"2\"><a href=\"/accept_invitation/{invitation}\">Accept</a>&nbsp;<a href=\"/reject_invitation/{invitation}\">Reject</a></td></tr>"
        leave += f"<tr><td colspan\"2\"><a href=\"/event/{event.id}\">Details</a></td></tr>"
    else:
        leave = ""
    return f'<table class="table"><thead><tr><th colspan="2">{event.title}</th></tr></thead><tbody><tr><td>Description</td><td>{event.description}</td></tr><tr><td>Location</td><td>{location}</td></tr><tr><td>Time/date</td><td>{time_date}</td></tr>{leave}</tbody></table>'

def is_admin():
    return User.query.get(me()).level == 3

def is_premium():
    return User.query.get(me()).level >= 2

def is_moderator(ev):
    return any(User.query.get(me()) in c.moderators for c in Event.query.get(ev).categories)

def is_manager(ev):
    return (Ev_att.query.filter_by(event_id=ev, attendee_id=me(), level=2).count() > 0) \
        or (Event.query.get(ev).owner_id == me())

def is_attendee(ev):
    return (Ev_att.query.filter_by(event_id=ev, attendee_id=me(), level=2).count() > 0) \
        or (Event.query.get(ev).owner_id == me())

@meetup.route('/profile')
@logged_only
def profile():
    owned_events_html = ""
    owned_events = Event.query.filter_by(owner_id=me())
    for owned_event in owned_events:
        owned_events_html += "<br>" + event_html(owned_event, detail=False)
    managed_events_html = ""
    managed_events = Event.query.join(Ev_att).filter_by(attendee_id=me(), level=2)
    for managed_event in managed_events:
        managed_events_html += "<br>" + event_html(managed_event, detail=False)
    attended_events_html = ""
    attended_events = Event.query.join(Ev_att).filter_by(attendee_id=me(), level=1)
    for attended_event in attended_events:
        attended_events_html += "<br>" + event_html(attended_event, detail=False)
    invited_events_html = ""
    invited_events = Invitation.query.filter_by(invitee_id=me())
    for invited_event in invited_events:
        invited_events_html += f"<br><strong>{invited_event.inviter.name}</strong> invited you to {event_html(invited_event.event)}"
    return render_template('profile.html', owned_events=owned_events_html, managed_events=managed_events_html,
                           attended_events=attended_events_html, invited_events=invited_events_html)

@meetup.route('/leave_event/<int:ev>')
@logged_only
def leave_event(ev):
    for ev_att in Ev_att.query.filter_by(attendee_id=me(), event_id=ev):
        db.session.delete(ev_att)
    db.session.commit()
    return profile()

@meetup.route('/request_attendance/<int:ev>')
@logged_only
def request_attendance(ev):
    db.session.add(Request(me(), ev))
    db.session.commit()
    return redirect(url_for('events_view'))

@meetup.route('/reject_invitation/<int:invitation>')
@logged_only
def reject_invitation(invitation):
    invitation_ = Invitation.query.get(invitation)
    if invitation_.invitee_id == me():
        db.session.delete(Invitation.query.get(invitation))
        db.session.commit()
    return redirect(url_for('profile'))

@meetup.route('/accept_invitation/<int:invitation>')
@logged_only
def accept_invitation(invitation):
    invitation_ = Invitation.query.get(invitation)
    if invitation_ and (invitation_.invitee_id == me()):
        if Ev_att.query.filter_by(event_id=invitation_.event_id, attendee_id=me()).count() == 0:
            db.session.add(Ev_att(invitation_.event_id, me(), 1))
        db.session.delete(Invitation.query.get(invitation))
        db.session.commit()
    return profile()

@meetup.route('/users')
@logged_only
def users():
    table  = ""
    for user in User.query.all():
        table += f"<tr><td>{user.id}</td><td>{user.name}</td><td>"
        if user.level == 1:
            table += "free"
        elif user.level == 2:
            table += "premium"
        elif user.level == 3:
            table += "administrator"
        print(user.__dict__)
        if user.address_id:
            table += "</td><td>" + location_html(user.address_id) + "</td>"
        else:
            table += "</td><td></td>"
        if user.id == me():
            table += f"<td><a href=\"/update_user/{user.id}\">Update</a>&nbsp;<a href=\"/user_categories/{user.id}\">Categories</a></td></tr>"
        elif is_admin():
            table += "<td><a href=\"/update_user/{friend.id}\">Update</a>&nbsp;<a href=\"/user_categories/{user.id}\">Categories</a></td></tr>"
        else:
            table += "<td><a href=\"/user_categories/{friend.id}\">Categories</a></td></tr>"
    return render_template('users.html', table=table)

@meetup.route('/update_user/<int:user>')
@logged_only
def update_user(user):
    user_ = User.query.get(user)
    free = " selected" if user_.level == 1 else ""
    premium = " selected" if user_.level == 2 else ""
    administrator = " selected" if user_.level == 3 else ""
    return render_template('update_user.html', user=user_,
                           free=free, premium=premium, administrator=administrator,
                           location_select_address=location_select(user_.address_id))


@meetup.route('/update_user_do')
@logged_only
def update_user_do():
    id_        = int(request.args.get('id_'))
    name       = request.args.get('name')
    level      = int(request.args.get('level'))
    address_id = int(request.args.get('location'))
    if is_admin() or id_ == me():
        User.query.filter_by(id=id_).update({User.name: name, User.level: level, User.address_id: address_id})
        db.session.commit()
        return users()
    else:
        return error_html("Illegal operation: Update user") + users()

@meetup.route('/user_categories/<int:user>')
@logged_only
def user_categories(user):
    user_ = User.query.get(user)
    categories_html = ""
    for category in Category.query.all():
        categories_html += "<tr><td>" + category.name + "</td><td>"
        if category in user_.subscriptions:
            events_ = Event.query.join(ev_cat).filter_by(category_id=category.id)
            for event in events_:
                categories_html += event_html(ev) + "<br>"
            if is_admin() or user == me():
                categories_html += f"</td><td><a href=\"/unsubscribe/{category.id}/{user}\">Unsubscribe</a></td></tr>"
            else:
                categories_html += "</td><td></td></tr>"
        else:
            if is_admin() or user == meetup.me():
                categories_html += f"</td><td><a href=\"/subscribe/{category.id}/{user}\">Subscribe</a></td></tr>"
            else:
                categories_html += "</td><td></td></tr>"
    return render_template('user_categories.html', categories=categories_html)

@meetup.route('/unsubscribe/<int:category>/<int:user>')
@logged_only
def unsubscribe(category, user):
    if is_admin() or user == me():
        category = Category.query.get(category)
        User.query.get(user).subscriptions.remove(category)
        db.session.commit()
        return user_categories(user)
    else:
        return error_html("Illegal operation: Unsubscribe") + user_categories(user)

@meetup.route('/subscribe/<int:category>/<int:user>')
@logged_only
def subscribe(category, user):
    user_ = User.query.get(user)
    if is_admin() or user == me():
        if user_.level == 1:
            if len(user_.subscriptions) > 2:
                return error_html("Illegal operation: Subscribe<br>\n") + user_categories(user)
        user_.subscriptions.append(Category.query.get(category))
        db.session.commit()
        return user_categories(user)
    else:
        return error_html("Illegal operation: Subscribe") + user_categories(user)

@meetup.route('/categories')
@logged_only
def categories():
    table_html = ""
    for category in Category.query.all():
        if is_admin():
            table_html += f"<tr><td>{category.name}</td><td><a href=\"/delete_category/{category.id}\">Delete</a>&nbsp;<a href=\"/update_category/{category.id}\">Update</a>&nbsp;<a href=\"/category/{category.id}\">Details</a></td></tr>"
        else:
            table_html += "<tr><td>" + str(category.name) + "</td><td></td></tr>"
    if is_admin():
        return render_template('categories.html', table=table_html)
    else:
        return render_template('categories_nonadmin.html', table=table_html)

@meetup.route('/delete_category/<int:cat>')
@logged_only
def delete_category(cat):
    if is_admin():
        db.session.delete(Category.query.get(cat))
        db.session.commit()
        return redirect(url_for('categories'))
    else:
        return error_html("Illegal operation: Delete category") + categories()

@meetup.route('/add_category')
@logged_only
def add_category():
    if is_admin():
        db.session.add(Category(request.args.get('name'), me()))
        db.session.commit()
        return redirect(url_for('categories'))
    else:
        return error_html("Illegal operation: Add category") + categories()

@meetup.route('/update_category/<int:cat>')
@logged_only
def update_category(cat):
    category = Category.query.get(cat)
    return render_template('update_category.html', category=category)

@meetup.route('/update_category_do')
@logged_only
def update_category_do():
    if not is_admin():
        return error_html("Illegal operation: Update category") + categories()
    Category.query.filter_by(id=int(request.args.get('id_'))).update({Category.name: request.args.get('name')})
    db.session.commit()
    return redirect(url_for('categories'))

@meetup.route('/category/<int:cat>')
@logged_only
def category(cat):
    category_ = Category.query.get(cat)
                      
    is_subscriber = category_ in User.query.get(me()).subscriptions
    moderators_html = ""
    subscribers_html = ""
    modify_html = ""
    events_html = ""
    if is_subscriber:
        if is_admin() or is_moderator(cat):
            modify_html = f'<div class="card-body"><a href="/category_moderators/{cat}">Modify</a></div>'
        for moderator in category_.moderators:
            moderators_html += f"<tr><td>{moderator.id}</td><td>{moderator.name}</td></tr>"
        for subscriber in category_.subscribers:
            subscribers_html += f"<tr><td>{subscriber.id}</td><td>{subscriber.name}</td></tr>"
    for event in category_.events:
        events_html += event_html(ev)
    return render_template('category.html', moderators=moderators_html, subscribers=subscribers_html,
                           modify=modify_html, Event=events_html, name=category_.name)

@meetup.route('/category_moderators/<int:cat>')
@logged_only
def category_moderators(cat):
    if is_admin():
        name = Category.get(cat).name
        for user in User.all():
            if cat_mod.filter(and_(cat_mod.category_id == cat, cat_mod.user_id == user.id)).count() > 0:
                current_html += f"<tr><td>{user.id}</td><td>{user.name}</td><td><a href=\"/delete_category_moderator/{cat}/{id}\">Remove moderator</a></td></tr>"
            else:
                new_html += f"<tr><td>{user.id}</td><td>{user.name}</td><td><a href=\"/add_category_moderator/{cat}/{user.id}\">Make moderator</a></td></tr>"
        return render_template('category_moderators.html', current=current_html, new=new_html)
    else:
        return error_html("Illegal operation: Category moderators") + category(cat)
        
@meetup.route('/delete_category_moderator/<int:cat>/<int:user>')
@logged_only
def delete_category_moderator(cat, user):
    if is_admin():
        cat_mod.delete().where(and_(cat_mod.category_id == cat, cat_mod.user_id == user))
        db.session.commit()
        return category_moderators(cat)
    else:
        return error_html("Illegal operation: Delete category moderator") + category(cat)

@meetup.route('/add_category_moderator/<int:cat>/<int:user>')
@logged_only
def add_category_moderator(cat, user):
    if is_admin():
        cat_mod.insert().values(category_id_=cat, user_id=user)
        return category_moderators(cat)
    else:
        return error_html("Illegal operation: Add category moderator") + category(cat)

@meetup.route('/events')
@logged_only
def events_view():
    return events_from(0)

@meetup.route('/events/<int:start>')
@logged_only
def events_from(start):
    events_html = ""
    c = Event.query.count()
    for event in Event.query.all()[::-1][start:start+5]:
        events_html += event_html(event) + "<br>"
    if (start > 0) or (start+5 < c):
        events_html = '</ul></nav>' + events_html
        if start+5 < c:
            events_html = f'<li class="page-item"><a class="page-link" href=\"/events/{start+5}">Events {start+6} -...</a></li>' + events_html
        events_html = f'<li class="page-item active"><a class="page-link" href="#">Events {start+1}-{start+5}</a></li>' + events_html
        if start > 0:
            events_html = f'<li class="page-item"><a class="page-link" href="/events/{start-5}">Events {start-4}-{start}</a></li>' + events_html
        events_html = '<nav><ul class="pagination">' + events_html
    return render_template('events_from.html', events=events_html, location_select=location_select(0))

@meetup.route('/add_event')
@logged_only
def add_event():
    event = Event(request.args.get('title'), request.args.get('description'), me(),
                  location_id=int(request.args.get('location')), time=request.args.get('time'),
                  date=request.args.get('date'))
    user = User.query.get(me())
    if user.level == 1 and len(user.owned_events) > 2:
        return error_html("Illegal operation: Add event") + events_view()
    else:
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events_view'))

@meetup.route('/event/<int:ev>')
@logged_only
def event(ev):
    evt = Event.query.get(ev)
    evt_html = event_html(evt)
    managers_html = ""
    attendees_html = ""
    requesters_html = ""
    categories_html = ""
    is_manager_ = is_manager(ev) or (evt.owner_id == me() and is_premium())
    is_moderator_ = is_moderator(ev)
    for ev_att in Ev_att.query.filter_by(event_id=ev, level=2):
        managers_html += f'<tr><td>{ev_att.attendee.id}</td><td>{ev_att.attendee.name}</td>'
        if evt.owner_id == me() and is_premium():
            managers_html += f'<td><a href=\"/revoke_manager/{ev}/{ev_att.attendee.id}">Revoke</a></td></tr>'
        else:
            managers_html += "<td></td></tr>"
    if is_attendee(ev) or (is_manager(ev) or is_premium()):
        for ev_att in Ev_att.query.filter_by(event_id=ev, level=1):
            attendees_html += f'<tr><td>{ev_att.attendee.id}</td><td>{ev_att.attendee.name}</td>'
            if is_manager(ev) or (evt.owner == me() and is_premium()):
                attendees_html += f'<td><a href=\"/promote_attendee/{ev}/{ev_att.attendee.id}">Promote to manager</a></td></tr>'
            else:
                attendees_html += "<td></td></tr>"
    if is_manager_:
        for request in Request.query.filter_by(event_id=ev):
            requesters_html += f'<tr><td>{request.requester.id}</td><td>{request.requester.name}</td><td><a href="/accept_request/{ev}/{request.requester.id}">Accept</a>&nbsp;<a href="/reject_request/{ev}/{request.requester.id}">Reject</a>&nbsp;</td></tr>'
        for category in Category.query.all():
            if evt in category.events:
                categories_html += f'<tr><td>{category.name} (selected)</td><td><a href=\"/delete_event_category/{ev}/{category.id}">Delete</td></tr>'
            else:
                categories_html += f'<tr><td>{category.name}</td><td><a href=\"/add_event_category/{ev}/{category.id}">Add</td></tr>'
    return render_template('event.html', is_manager=is_manager_, is_moderator=is_moderator_, event=evt_html,
                           managers=managers_html, attendees=attendees_html, requesters=requesters_html,
                           categories=categories_html, ev=ev)

@meetup.route('/add_event_category/<int:ev>/<int:cat>')
@logged_only
def add_event_category(ev, cat):
    if is_manager(ev):
        evt = Event.query.get(ev)
        category = Category.query.get(cat)
        evt.categories.append(category)
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Add event category") + event(ev)

@meetup.route('/delete_event_category/<int:ev>/<int:cat>')
@logged_only
def delete_event_category(ev, cat):
    if is_manager(ev):
        evt = Event.query.get(ev)
        category = Category.query.get(cat)
        evt.categories.remove(category)
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Delete event category") + event(ev)

@meetup.route('/delete_event/<int:ev>')
@logged_only
def delete_event(ev):
    if is_manager(ev):
        db.session.delete(Event.query.get(ev))
        db.session.commit()
        return events_view()
    else:
        return error_html("Illegal operation: Delete event") + events_view()

@meetup.route('/update_event/<int:ev>')
@logged_only
def update_event(ev):
    evt = Event.query.get(ev)
    location = location_select(evt.location_id or 0)
    return render_template('update_event.html', event=evt, location=location)

@meetup.route('/update_event_do')
@logged_only
def update_event_do():
    id_ = request.args.get('id_')
    if not (is_manager(id_) or is_moderator(id_)):
        return error_html("Illegal operation: Update event") + event(id_)
    else:
        title       = request.args.get('title')
        description = request.args.get('description')
        location    = int(request.args.get('location')) if request.args.get('location') else None
        time        = request.args.get('time')
        date        = request.args.get('date')
        owner       = int(request.args.get('owner'))
        Event.query.filter_by(id=id_).update({Event.title: request.args.get('title'),
                                              Event.description: request.args.get('description'),
                                              Event.location_id: request.args.get('location'),
                                              Event.time: request.args.get('time'),
                                              Event.date: request.args.get('date'),
                                              Event.owner_id: request.args.get('owner')})
        db.session.commit()
        return event(id_)

@meetup.route('/promote_attendee/<int:ev>/<int:att>')
@logged_only
def promote_attendee(ev, att):
    evt = Event.query.get(ev)
    if is_manager(ev) or (evt.owner == me() and is_premium()):
        Ev_att.query.filter_by(event_id=ev, attendee_id=att).update({Ev_att.level: 2})
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Promote attendee") + event(ev)

@meetup.route('/revoke_manager/<int:ev>/<int:att>')
@logged_only
def revoke_manager(ev, att):
    evt = Event.query.get(ev)
    if is_manager(ev) or (evt.owner == me() and is_premium()):
        Ev_att.query.filter_by(event_id=ev, attendee_id=att).update({Ev_att.level: 1})
        return event(ev)
    else:
        return error_html("Illegal operation: Revoke manager") + event(ev)

@meetup.route('/accept_request/<int:ev>/<int:req>')
@logged_only
def accept_request(ev, req):
    if is_manager(ev):
        for request in Request.query.filter_by(event_id=ev, requester_id=req).all():
            db.session.delete(request)
        if Ev_att.query.filter_by(event_id=ev, attendee_id=req).count() == 0:
            db.session.add(Ev_att(ev, req, 1))
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Accept request") + event(ev)

@meetup.route('/reject_request/<int:ev>/<int:req>')
@logged_only
def reject_request(ev, req):
    if is_manager(ev):
        for request in Request.query.filter_by(event_id=ev, requester_id=req).all():
            db.session.delete(request)
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Reject request") + event(ev)

@meetup.route('/invite/<int:ev>')
@logged_only
def invite(ev):
    if is_manager(ev):
        db.session.add(Invitation(me(), request.args.get('ID'), ev))
        db.session.commit()
        return event(ev)
    else:
        return error_html("Illegal operation: Invite") + event(ev)

@meetup.route('/locations')
@logged_only
def locations():
    table_html = ""
    for location in Location.query.all():
        table_html += f'<tr><td>{location.name} ({location.country})</td>'
        if location.owner_id == me():
            table_html += f'<td><a href=\"/delete_location/{location.id}">Delete</a>&nbsp;<a href="/update_location/{location.id}">Update</a></td></tr>'
        else:
            table_html += '<td></td></tr>'
    return render_template('locations.html', table=table_html)

@meetup.route('/delete_location/<int:location>')
@logged_only
def delete_location(location):
    location_ = Location.query.get(location)
    if location_.owner_id != me():
        return error_html("Illegal operation: Delete location") + Location()
    else:
        db.session.delete(location_)
        db.session.commit()
        return locations()

@meetup.route('/add_location')
@logged_only
def add_location():
    db.session.add(Location(request.args.get('name'), request.args.get('country'), me()))
    db.session.commit()
    return locations()

@meetup.route('/update_location/<int:location>')
@logged_only
def update_location(location):
    location_ = Location.query.get(location)
    return render_template('update_location.html', location=location_)

@meetup.route('/update_location_do')
@logged_only
def update_location_do():
    id_ = int(request.args.get('id_'))
    if Location.query.get(id_).owner_id != me():
        return error_html("Illegal operation: Update location") + locations()
    else:
        Location.query.filter_by(id=id_).update({Location.name: request.args.get('name'),
                                                 Location.country: request.args.get('country')})
        db.session.commit()
        return redirect(url_for('locations'))

@meetup.route('/login', methods=['POST'])
def login():
    # Should not be accessed by an already logged-in user
    if 'user_id' in session:
        return redirect(url_for('index'))
    # If not logged in
    if request.method == 'POST':
        name  = request.form['name']
        hash_ = hashing.hash_value(request.form['password'])
        user = User.query.filter_by(name=name, password=hash_).one_or_none()
        if user:
            session['user_id']   = user.id
            session['user_name'] = user.name
            return redirect(url_for('index'))
    # Login failed, redirect to index
    return redirect(url_for('index', wrong_pass=True))

@meetup.route('/logout')
@logged_only
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('user_name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    # set this to False for evaluation
    meetup.run(debug=True)
