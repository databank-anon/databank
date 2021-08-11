from flask import Flask, render_template, request, session, url_for, redirect, escape
import subprocess
import os
import sys

from settings import *

if __name__ == '__main__':
    for param in sys.argv[1:]:
        if param == "-m":
            # show monitor trace
            set_option('verbose_monitor')
        elif param == "-d":
            # show database trace
            set_option('verbose_db')
        elif param == "-p":
            # make application passive (no labelling or monitoring)
            set_option('passive')
        elif param == "-sp":
            # make application semi-passive (labelling but no monitoring)
            set_option('semipassive')
        elif param == "-t":
            # compute monitoring trace and dump it on failure
            set_option('trace')

from catalog import user_catalog
from databank.monitor import monitors, Monitor

## Index, login, logout

@bank.route('/', methods=['GET'])
def index():
    # Data from current session
    user_id = session.get('user_id', None)
    user_name = session.get('user_name', None)
    # Failed authentication
    wrong_pass = request.args.get('wrong_pass', None)
    # Catalog
    if user_id:
        apps = user_catalog(user_id)
    # Render index
    return render_template("index.html", **locals())

@bank.route('/login', methods=['POST'])
def login():
    # Should not be accessed by an already logged-in user
    if 'user_id' in session:
        return redirect(url_for('index'))
    # If not logged in
    if request.method == 'POST':
        name  = request.form['name']
        hash_ = hashing.hash_value(request.form['password'])
        query = "SELECT * FROM users WHERE name = ? AND hash = ?"
        cur = get_db().execute(query, [name, hash_])
        res = cur.fetchall()
        cur.close()
        if res:
            session['user_id']   = res[0][0]
            session['user_name'] = res[0][1]
            session['user_apps'] = [app.id_ for app in user_catalog(res[0][0])]
            # Log in, redirect to index
            return redirect(url_for('index'))
    # Login failed, redirect to index
    return redirect(url_for('index', wrong_pass=True))

@bank.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('user_name', None)
    return redirect(url_for('index'))

## Profile editor

@bank.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    status = request.args.get('status', "0")
    name = session.get('user_name')
    return render_template("profile.html", **locals())

@bank.route('/profile/change_name', methods=['POST'])
def change_name():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    name = request.form['name']
    query = "UPDATE users SET name = ? WHERE id = ?"
    con = get_db()
    con.execute(query, [name, session['user_id']])
    con.commit()
    session['user_name'] = name
    return redirect(url_for('profile', status=2))

@bank.route('/profile/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    password = request.form['password']
    repeat = request.form['repeat']
    if password == repeat:
        hash_ = hashing.hash_value(request.form['password'])
        query = "UPDATE users SET hash = ? WHERE id = ?"
        con = get_db()
        con.execute(query, [hash_, session['user_id']])
        con.commit()
        return redirect(url_for('profile', status=1))
    return redirect(url_for('profile', status=-1))

## Policy editor

@bank.route('/policy')
def policy():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    query = ("SELECT policy FROM users WHERE id = ?")
    cur = get_db().execute(query, [session['user_id']])
    policy = cur.fetchall()[0][0]
    cur.close()
    return render_template("policy.html", **locals())

@bank.route('/policy/check', methods=['POST'])
def policy_check():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    temp_filename = TEMP_POLICY.format(user_id)
    policy = request.form['policy'].strip()
    with open(temp_filename, "w") as f:
        f.write(policy)
    try:
        if policy:
            o = subprocess.check_output(
                [MONPOLY, "-formula", temp_filename, "-sig", SIG, "-check", "-databank"],
                stderr=subprocess.STDOUT
            )
        output = ('Your new policy is checked. '
                  'You can now <a href="javascript:save()">save</a> it.')
    except subprocess.CalledProcessError as e:
        output = '<span class="error">{}</span>'.format(e.output.decode("utf-8"))
    subprocess.call(["rm", temp_filename])
    return output.replace("\n", "<br>")

@bank.route('/policy/save', methods=['POST'])
def policy_save():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    policy = request.form['policy'].strip()
    query = "UPDATE users SET policy = ? WHERE id = ?"
    con = get_db()
    con.execute(query, [policy, session['user_id']])
    con.commit()
    if os.path.isfile(monitors[user_id].state_fn):
        os.remove(monitors[user_id].state_fn)
    monitors[user_id] = Monitor(user_id, policy)
    return redirect(url_for('policy'))

if __name__ == '__main__':
    bank.run(debug=True, use_reloader=False)
