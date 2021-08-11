from subprocess import Popen, DEVNULL, STDOUT, run
import os, signal
import os.path
import time
import random, string
import sqlite3
from shutil import copyfile, move
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

def random_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

DATABANK = "main.py"
FLASK = "collection/baseline/meetup/meetup.py"

_time = time

DB = "../db/database.db"
DB_SAVE = "../evaluation/save/database.db_save"
DB_FLASK = "collection/baseline/meetup/database.db"
DB_FLASK_SAVE = "../evaluation/save/database_flask.db_save"
DB_FUNDAMENTAL = "../db/fundamental.db"
STATE = "../monitor_files"
STATE_SAVE = "../evaluation/save"
EVALUATION = "../evaluation"
MONITOR_FILES = "../monitor_files"

TIME = "../evaluation/time.json"
TIME_SAVE = "../evaluation/save/time.json_save"
LOG  = "../evaluation/log.json"

POLICIES = ['FALSE', # trivial policy
            'EXISTS u,l. Learns(u, l) AND NOT (u = "{0}") AND EXISTS f, v. ONCE(1209600,*) Inputs("2/add_event", f, l, v)',    # small policy
            'EXISTS u, l. (Learns(u, l) AND (ONCE (EXISTS a, v. Inputs("2/add_event", a, l, v))) AND ((NOT EXISTS m. Inputs("2/add_friend", "ID", m, u) OR Inputs("2/delete_friend", "user", m, u)) SINCE (EXISTS m. Inputs("2/delete_friend", "user", m, u))) AND NOT u = "{0}") OR (Learns(u, l) AND (ONCE (EXISTS a, v. Inputs("2/add_event", a, l, v))) AND (NOT ONCE EXISTS m. Inputs("2/add_friend", "ID", m, u)) AND NOT u = "{0}")'] # medium policy

PASSWORD_HASH = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

t = _time.time()
c = 0
def progress():
    global c
    c += 1
    print(f"{_time.time()-t:.2f}s; {c} it")
    

def clear_create_random_event_databank():
    
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute("DELETE FROM '2_events' WHERE 1=1")
    cur.execute("DELETE FROM '2_events_inputs_' WHERE 1=1")
    cur.execute("DELETE FROM '2_events_new_' WHERE 1=1")
    db.commit()
    db.close()

def clear_invite_to_random_event_databank():
    
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute("DELETE FROM '2_events' WHERE 1=1")
    cur.execute("DELETE FROM '2_events_inputs_' WHERE 1=1")
    cur.execute("DELETE FROM '2_events_new_' WHERE 1=1")
    cur.execute("DELETE FROM '2_invitations' WHERE 1=1")
    cur.execute("DELETE FROM '2_invitations_inputs_' WHERE 1=1")
    cur.execute("DELETE FROM '2_invitations_new_' WHERE 1=1")
    cur.execute("DELETE FROM '2_ev_att' WHERE 1=1")
    cur.execute("DELETE FROM '2_ev_att_inputs_' WHERE 1=1")
    cur.execute("DELETE FROM '2_ev_att_new_' WHERE 1=1")
    db.commit()
    db.close()
    
def clear_create_random_event_flask():
    
    db = sqlite3.connect(DB_FLASK)
    cur = db.cursor()
    cur.execute("DELETE FROM 'event' WHERE 1=1")
    db.commit()
    db.close()

def clear_invite_to_random_event_flask():
    
    db = sqlite3.connect(DB_FLASK)
    cur = db.cursor()
    cur.execute("DELETE FROM 'event' WHERE 1=1")
    cur.execute("DELETE FROM 'invitation' WHERE 1=1")
    cur.execute("DELETE FROM 'ev_att' WHERE 1=1")
    db.commit()
    db.close()

def save_state():

    if os.path.exists(DB):
        copyfile(DB, DB_SAVE)
    if os.path.exists(DB_FLASK):
        copyfile(DB_FLASK, DB_FLASK_SAVE)
    for state in os.listdir(STATE):
        if state[:6] == "state-":
            copyfile(os.path.join(STATE, state), os.path.join(STATE_SAVE, state + "_save"))

def restore_state():
    
    if os.path.exists(DB_SAVE):
        copyfile(DB_SAVE, DB)
    if os.path.exists(DB_FLASK_SAVE):
        copyfile(DB_FLASK_SAVE, DB_FLASK)
    for state in os.listdir(STATE):
        if os.path.exists(os.path.join(STATE_SAVE, state + "_save")) and state[:6] == "state-":
            copyfile(os.path.join(STATE_SAVE, state + "_save"), os.path.join(STATE, state))

def monitoring_memory():
    mem = 0
    for state in os.listdir(STATE):
        if state[:6] == "state-":
            mem += os.path.getsize(os.path.join(STATE, state))
    return mem

TIMEOUT = 1000

def _(f, *args, **kwargs):
    for _ in range(TIMEOUT):
        try:
            return f(*args, **kwargs)
        except:
            pass
            #print(f"Retrying for f={f} x={x}")
    raise Exception

def __(f):
    for _ in range(TIMEOUT):
        try:
            return f()
        except:
            pass
            #print(f"Retrying for f={f} x={x}")
    raise Exception


def login(my_name, my_password, flask):

    global _

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://localhost:5000")
    
    # log in as user test

    name = _(driver.find_element_by_name, "name")
    name.send_keys(my_name)
    password = _(driver.find_element_by_name, "password")
    password.send_keys(my_password)
    submit = _(driver.find_element_by_tag_name, "button")
    submit.click()

    if not flask:
        # open meetup

        meetup = _(driver.find_element_by_link_text, "Meetup")
        meetup.click()
        
    return driver
    
def logout(driver, flask):

    if not flask:
        back = _(driver.find_element_by_link_text, "Back to the Databank")
        __(back.click)
    logout_ = _(driver.find_element_by_link_text, "Log out")
    __(logout_.click)

    driver.quit()
    
def build_report(total_time, metadata, flask):

    if flask:
        report = {**{'total_time'       : total_time,
                     'database_memory'  : os.path.getsize(DB),
                     'monitoring_memory': monitoring_memory()},
                  **metadata}
    else:
        with open(TIME_SAVE, 'r') as f:
            js = json.load(f)

        report = {**{'total_time'       : total_time,
                     'database_time'    : js["database"],
                     'database_memory'  : os.path.getsize(DB),
                     'monitoring_memory': monitoring_memory()},
                  **metadata}

        if "monitoring" in js:
            report['monitoring_time'] = js["monitoring"]
                  
    return report

def get_latency(driver):
    
    request_start = driver.execute_script("return window.performance.timing.requestStart")
    response_start = driver.execute_script("return window.performance.timing.responseStart")
    return (response_start - request_start) / 1000

def restore_time():
    
    if os.path.exists(TIME_SAVE):
        copyfile(TIME_SAVE, TIME)
    elif os.path.exists(TIME):
        os.remove(TIME)

def save_time():

    if os.path.exists(TIME):
        copyfile(TIME, TIME_SAVE)

def create_random_events_databank(n, metadata=None, flask=False):

    global _time, _
    
    driver = login("Alice", "test", flask)

    # open events

    events = _(driver.find_element_by_link_text, "Events")
    events.click()

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)
        
    total_time = 0
    
    # create new event with random content
    
    for c in range(n):
        title = _(driver.find_element_by_name, "title")
        if c > 0:
            save_time()
            total_time += get_latency(driver)
        title.send_keys(random_string())
        description = _(driver.find_element_by_name, "description")
        description.send_keys(random_string())
        time = _(driver.find_element_by_name, "time")
        time.send_keys(random_string())
        date = _(driver.find_element_by_name, "date")
        date.send_keys(random_string())
        submit = _(driver.find_element_by_class_name, "btn")
        restore_time()
        __(submit.click)

    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    save_time()
    total_time += get_latency(driver)
    __(back.click)

    logout(driver, flask)
    
    if metadata is None:
        return
    
    return build_report(total_time, metadata, flask)

def add_friendship(user_name, friend_id):

    driver = login(user_name, "test", False)

    # open users
    users = _(driver.find_element_by_link_text, "Users")
    users.click()

    # add friendship
    ID = _(driver.find_element_by_name, "ID")
    ID.send_keys(str(friend_id))
    submit = _(driver.find_element_by_class_name, "btn")
    submit.click()

    # back and logout
    
    back = _(driver.find_element_by_link_text, "Meetup")
    back.click()
    
    logout(driver, False)
    
def delete_events_databank(n, metadata, flask=False):

    global _time, _
    
    driver = login("Alice", "test", flask)

    # open events

    events = _(driver.find_element_by_link_text, "Events")
    events.click()

    # find all events details links

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)

    total_time = 0
    
    details = _(driver.find_elements_by_link_text, "Details")
    assert(len(details) >= n)
    for c in range(n):
        detail = _(driver.find_elements_by_link_text, "Details")[0]
        if c > 0:
            save_time()
            total_time += get_latency(driver)
        detail.click()
        delete = _(driver.find_element_by_link_text, "Delete")
        restore_time()
        __(delete.click)
        
    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    save_time()
    total_time += get_latency(driver)
    __(back.click)
        
    logout(driver, flask)

    return build_report(total_time, metadata, flask)
    
def view_events_databank(n, metadata, flask=False):

    global _time, _
    
    driver = login("Alice", "test", flask)

    # open events

    events = _(driver.find_element_by_link_text, "Events")
    events.click()

    # find all events details links

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)

    total_time = 0
    
    details = _(driver.find_elements_by_link_text, "Details")
    assert(len(details) >= n)
    for c in range(n):
        detail = _(driver.find_elements_by_link_text, "Details")[c]
        restore_time()
        __(detail.click)
        save_time()
        total_time += get_latency(driver)
        back = _(driver.find_element_by_link_text, "Back to events")
        __(back.click)
        
    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    back.click()
    
    logout(driver, flask)

    return build_report(total_time, metadata, flask)
    
def list_events_databank(metadata, flask=False):

    global _time, _
    
    driver = login("Alice", "test", flask)

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)
        
    # open profile

    profile = _(driver.find_element_by_link_text, "Your profile")
    restore_time()
    __(profile.click)
    total_time = get_latency(driver)
    save_time()
    
    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    __(back.click)
    
    logout(driver, flask)
    
    return build_report(total_time, metadata, flask)

def list_events_paginated_databank(metadata, flask=False):

    global _time, _
    
    driver = login("Alice", "test", flask)

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)
        
    # open profile

    events = _(driver.find_element_by_link_text, "Events")
    restore_time()
    __(events.click)
    total_time = get_latency(driver)
    save_time()
    
    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    __(back.click)
    
    logout(driver, flask)
    
    return build_report(total_time, metadata, flask)
   
def invite_to_random_event_databank(metadata, flask=False):

    global _time

    driver = login("Bob", "test", flask)

    if os.path.exists(TIME_SAVE):
        os.remove(TIME_SAVE)

    # open events

    events = _(driver.find_element_by_link_text, "Events")
    events.click()

    # create new event with random content

    title = _(driver.find_element_by_name, "title")
    title.send_keys(random_string())
    description = _(driver.find_element_by_name, "description")
    description.send_keys(random_string())
    time = _(driver.find_element_by_name, "time")
    time.send_keys(random_string())
    date = _(driver.find_element_by_name, "date")
    date.send_keys(random_string())
    submit = _(driver.find_element_by_class_name, "btn")
    __(submit.click)

    # find newly added event in page

    event_detail = _(driver.find_elements_by_link_text, "Details")[0]
    event_detail.click()

    # invite user 2

    ID = _(driver.find_element_by_name, "ID")
    ID.send_keys("1")
    submit = _(driver.find_element_by_class_name, "btn")
    restore_time()
    __(submit.click)

    # back and logout

    back = _(driver.find_element_by_link_text, "Meetup")
    total_time = get_latency(driver)
    save_time()
    __(back.click)
    if not flask:
        back = _(driver.find_element_by_link_text, "Back to the Databank")
        back.click()
    logout_ = _(driver.find_element_by_link_text, "Log out")
    logout_.click()

    driver.quit()

    return build_report(total_time, metadata, flask)
    

### Main process

n_events   = [0, 0, 10, 25, 50, 100, 250, 500]
u_users    = [2, 10, 50, 100, 500]
p_policies = [0, 1, 2]
M = 10
M2 = 5

if os.path.exists(LOG):
    with open(LOG, 'r') as f:
        js = json.load(f)
else:
    js = []

def evaluate_fixed_u_p_m_i(u, p, mode, i, no_create=False):
    flask = mode == 'flask'
    print(f'Evaluate_fixed_u_p_m_i, u={u}, p={p}, mode={mode}, i={i}')
    # prepare consistent state with n_events[i] events
    restore_state()
    last_n = n_events[i]   
    prev_n = n_events[i-1]
    if not no_create:
        create_random_events_databank(last_n - prev_n, flask=flask)
        save_state()
    if last_n > 0:
        ## delete single entity
        # prepare metadata
        metadata = {'mode'    : mode,
                    'n_events': last_n,
                    'workload': 'delete',
                    'm2'      : M2,
                    'u'       : u,
                    'p'       : p}
        # run tests
        for m in range(M):
            restore_state()
            report = while_invalid(delete_events_databank, M2, metadata, flask=flask)
            js.append(report)
            progress()
            with open(LOG, 'w') as f:
                 json.dump(js, f)
        ## view single entity
        # prepare metadata
        metadata = {'mode'    : mode,
                    'n_events': last_n,
                    'workload': 'view',
                    'm2'      : M2,
                    'u'       : u,
                    'p'       : p}
        # run tests
        for m in range(M):
            restore_state()
            report = while_invalid(view_events_databank, M2, metadata, flask=flask)
            js.append(report)
            progress()
            with open(LOG, 'w') as f:
                json.dump(js, f)
    ## invite workload
    # prepare metadata
    metadata = {'mode'    : mode,
                'n_events': last_n,
                'workload': 'invite',
                'u'       : u,
                'p'       : p}
    # run tests
    for m in range(M):
        restore_state()
        report = while_invalid(invite_to_random_event_databank, metadata, flask=flask)
        js.append(report)
        progress()
        with open(LOG, 'w') as f:
            json.dump(js, f)
    ## list all events (in profile)
    # prepare metadata
    metadata = {'mode'    : mode,
                'n_events': last_n,
                'workload': 'list',
                'u'       : u,
                'p'       : p}
    # run tests
    for m in range(M):
       restore_state()
       report = while_invalid(list_events_databank, metadata, flask=flask)
       js.append(report)
       progress()
       with open(LOG, 'w') as f:
           json.dump(js, f)
           
    ## list all events (paginated)
    # prepare metadata
    metadata = {'mode'    : mode,
                'n_events': last_n,
                'workload': 'list_paginated',
                'u'       : u,
                'p'       : p}
    # run tests
    for m in range(M):
       restore_state()
       report = while_invalid(list_events_paginated_databank, metadata, flask=flask)
       js.append(report)
       progress()
       with open(LOG, 'w') as f:
           json.dump(js, f)

    ## insert single entity
    # prepare metadata
    metadata = {'mode'    : mode,
                'n_events': last_n,
                'workload': 'insert',
                'm2'      : M2,
                'u'       : u,
                'p'       : p}
    # run tests
    for m in range(M):
       restore_state()
       report = while_invalid(create_random_events_databank, M2, metadata=metadata, flask=flask)
       js.append(report)
       progress()
       with open(LOG, 'w') as f:
           json.dump(js, f)

def while_invalid(f, *args, **kwargs):
    while True:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("while_invalid: Error!")
            print(str(e))
            pass
        else:
            break

def evaluate_fixed_u_p_m(u, p, mode):
    if mode == 'flask':
        clear_create_random_event_flask()
        clear_invite_to_random_event_flask()
    else:
        clear_create_random_event_databank()
        clear_invite_to_random_event_databank()
    save_state()
    for i in range(1, len(n_events)):
        evaluate_fixed_u_p_m_i(u, p, mode, i)
        
def reset_users(u, p):
    users = ["Alice", "Bob"]
    while len(users) < u:
        users.append(f"Charlie{len(users) - 2}")
    #users = users[:2]
    policy = POLICIES[p]
    dbd = sqlite3.connect(DB_FUNDAMENTAL)
    dbf = sqlite3.connect(DB_FLASK)
    db = sqlite3.connect(DB)
    curd = dbd.cursor()
    curf = dbf.cursor()
    cur = db.cursor()
    curd.execute("DELETE FROM 'users' WHERE 1=1")
    curf.execute("DELETE FROM 'user' WHERE 1=1")
    cur.execute("DELETE FROM '2_friends' WHERE 1=1")
    cur.execute("DELETE FROM '2_friends_inputs_' WHERE 1=1")
    for i, user in enumerate(users):
        curd.execute(f"INSERT INTO 'users' (id, name, hash, policy) VALUES ({i+1}, '{user}', '{PASSWORD_HASH}', '{policy.format(i+1)}')")
        curf.execute(f"INSERT INTO 'user' (id, name, password, level, address_id) VALUES ({i+1}, '{user}', '{PASSWORD_HASH}', 3, 0)")
        with open(os.path.join(MONITOR_FILES, f"policy-{i+1}"), 'w') as f:
            f.write(policy)
    for state in os.listdir(STATE):
        if state[:6] == "state-":
            os.remove(os.path.join(STATE, state))
    dbd.commit()
    dbf.commit()
    db.commit()
    dbd.close()
    dbf.close()
    db.close()

def evaluate_fixed_u_p(u, p):
    reset_users(u, p)
    databank = Popen(["python3", DATABANK],
                     stdout=DEVNULL, stderr=STDOUT)
    time.sleep(4)
    add_friendship("Alice", 2)
    add_friendship("Bob", 1)
    save_state()
    evaluate_fixed_u_p_m(u, p, 'active')
    databank.kill()
    flask = Popen(["python3", FLASK],
                     stdout=DEVNULL, stderr=STDOUT)
    pid = flask.pid
    time.sleep(4)
    evaluate_fixed_u_p_m(u, p, 'flask')
    run(["kill", "-9", str(pid)])
    run(["kill", "-9", str(pid + 2)])
    run(["kill", "-9", str(pid + 3)])

def evaluate_fixed_u_i(u, i):
    # Evaluate, for each policy
    for p in p_policies:
        # Set policy
        reset_users(u, p)
        save_state()
        # Active
        clear_create_random_event_databank()
        clear_invite_to_random_event_databank()
        databank = Popen(["python3", DATABANK],
                         stdout=DEVNULL, stderr=STDOUT)
        time.sleep(4)
        add_friendship("Alice", 2)
        add_friendship("Bob", 1)
        create_random_events_databank(n_events[i])
        save_state()
        evaluate_fixed_u_p_m_i(u, p, 'active', i, no_create=True)
        databank.kill()
        # Flask
        clear_create_random_event_flask()
        clear_invite_to_random_event_flask()
        flask = Popen(["python3", FLASK],
                      stdout=DEVNULL, stderr=STDOUT)
        pid = flask.pid
        time.sleep(4)
        create_random_events_databank(n_events[i], flask=True)
        save_state()
        evaluate_fixed_u_p_m_i(u, p, 'flask', i, no_create=True)
        run(["kill", "-9", str(pid)])
        run(["kill", "-9", str(pid + 2)])
        run(["kill", "-9", str(pid + 3)])

def evaluate_fixed_p_i(p, i):
    # Evaluate, for each policy
    for u in u_users:
        # Set policy
        print('reset_users')
        reset_users(u, p)
        # Active
        clear_create_random_event_databank()
        clear_invite_to_random_event_databank()
        print('open databank')
        databank = Popen(["python3", DATABANK],
                         stdout=DEVNULL, stderr=STDOUT)
        time.sleep(4)
        add_friendship("Alice", 2)
        add_friendship("Bob", 1)
        create_random_events_databank(n_events[i])
        save_state()
        evaluate_fixed_u_p_m_i(u, p, 'active', i, no_create=True)
        databank.kill()
        # Flask
        clear_create_random_event_flask()
        clear_invite_to_random_event_flask()
        flask = Popen(["python3", FLASK],
                      stdout=DEVNULL, stderr=STDOUT)
        pid = flask.pid
        time.sleep(4)
        create_random_events_databank(n_events[i], flask=True)
        save_state()
        evaluate_fixed_u_p_m_i(u, p, 'flask', i, no_create=True)
        run(["kill", "-9", str(pid)])
        run(["kill", "-9", str(pid + 2)])
        run(["kill", "-9", str(pid + 3)])

evaluate_fixed_u_p(10, 1)
evaluate_fixed_u_i(10, 4)
evaluate_fixed_p_i(1, 4)
