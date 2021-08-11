# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from hashlib import md5
from datetime import datetime
#import os, sys
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Flask, request, session, url_for, redirect, render_template, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = "E4kB3BUlTXivYtkaKnCb9XHGIr9erSEIX0n0MWOnAqlqr2PGKWjPgWp2834M5PmDqx2dEvI2EV7YdriY"
hashing = Hashing(app)

PER_PAGE = 30

following = db.Table('following',
                     db.Column('follower', db.Text, db.ForeignKey('user.username'), nullable=False),
                     db.Column('followed', db.Text, db.ForeignKey('user.username'), nullable=False))

def logged_only(f):
    def wrapper(*args, **kwargs):
        if session.get('username', None) is None:
            abort(401)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.Text, nullable=False, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    pw_hash = db.Column(db.Text, nullable=False)
    timeline = db.relationship('Message', backref='author', lazy=True)
    followers = db.relationship('User', secondary=following,
                                primaryjoin=(following.c.follower == username),
                                secondaryjoin=(following.c.followed == username),
                                backref=db.backref('followed', lazy='subquery'))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.pw_hash = generate_password_hash(password)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column('id', db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, author_id, text, pub_date):
        self.author_id = author_id
        self.text = text
        self.pub_date = pub_date

def me():
    if session.get('username', None) is None:
        return None
    return session['username']

    
def get_public_timeline_messages():
    """Get public timeline message list."""
    return Message.query.limit(PER_PAGE).all()


def get_user_timeline_messages(username):
    """Get user time line message list."""
    return User.query.get(username).timeline[:PER_PAGE]

    
def add_message_to_user_timeline(username, message_id):
    """Add message id to user timeline messages list."""
    user = User.query.get(username)
    message = Message.query.get(message_id)
    followees = user.followers
    for followee in followees:
        followee.timeline.append(message)
    user.timeline.append(message)
    db.session.commit()

    
def push_message(author_id, text):
    """Add message and return its id."""
    message = Message(author_id, text, datetime.now())
    db.session.add(message)
    db.session.commit()
    return message.id


def get_followees(username):
    """Get list of user followers."""
    return User.query.get(username).followers


def follow(user1, user2):
    """Follow the specified user."""
    user = User.query.get(user2)
    user.followers.append(User.query.get(user1))
    db.session.commit()


def unfollow(user1, user2):
    """Unfollow the specified user."""
    user = User.query.get(user2)
    user.followers.remove(User.query.get(user1))
    db.session.commit()


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(float(timestamp)).strftime('%Y-%m-%d @ %H:%M')


@app.route('/')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if me() is None:
        return redirect(url_for('public_timeline'))
    messages = get_user_timeline_messages(me())
    user = User.query.get(me())
    return render_template('timeline.html', messages=messages, user=user)


@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    return render_template('timeline.html',
                           messages=get_public_timeline_messages(),
                           user=User.query.get(me()))


@app.route('/<username>')
def user_timeline(username):
    """Displays a user's tweets."""
    user = User.query.get(username)
    if not user:
        abort(401)
    followed = False
    me_user = None
    if me() is not None:
        me_user = User.query.get(me())
        followed = user in me_user.followed
    return render_template('timeline.html',
                           messages=get_user_timeline_messages(username),
                           followed=followed,
                           profile_user=user,
                           user=me_user)


@app.route('/<username>/follow')
@logged_only
def follow_user(username):
    """Adds the current user as follower of the given user."""
    user = User.query.get(username)
    if not user:
        abort(401)
    follow(me(), username)
    flash('You are now following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/<username>/unfollow')
@logged_only
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    user = User.query.get(username)
    if not user:
        abort(401)
    unfollow(me(), username)
    flash('You are no longer following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/add_message', methods=['POST'])
@logged_only
def add_message():
    """Registers a new message for the user."""
    if request.form['text']:
        message_id = push_message(me(), request.form['text'])
        add_message_to_user_timeline(me(), message_id)
        flash('Your message was recorded')
    return redirect(url_for('timeline'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if me() is not None:
        return redirect(url_for('timeline'))
    user = User.query.get(me())
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'])
        if user.count() == 0:
            error = 'Invalid username'
        else:
            user = user.one()
            if not check_password_hash(user.pw_hash,
                                     request.form['password']):
                error = 'Invalid password'
            else:
                flash('You were logged in')
                session['username'] = user.username
                return redirect(url_for('timeline'))
    return render_template('login.html', error=error, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if me() is not None:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif User.query.filter_by(username=request.form['username']).count() > 0:
            error = 'The username is already taken'
        else:
            user = User(request.form['username'],
                        request.form['email'],
                        request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    if me() is None:
        user = None
    else:
        user = User.query.get(me())
    return render_template('register.html', error=error, user=user)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('username', None)
    return redirect(url_for('public_timeline'))

if __name__ == '__main__':
    db.create_all()
    app.run()
