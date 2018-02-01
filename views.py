from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from Lynx import *
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///lynx.db', echo=False)

application = Flask(__name__)
print('\n*****','views','*****\n')

@app.route('/')
@app.route('/home')
def home():
    print('\n*****','home','*****\n')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = session.get('username')

        fetch_my_links(username)
        dictX = dict()
        j = 0
        myLinks = fetch_my_links(username)
        for l in myLinks:
            fou = dict()
            fou['link'] = l
            if l.endswith("jpg") or l.endswith("png") or l.endswith("gif"):
                fou['image'] = l
            else:
                fou['image'] = "/static/diffsite_logo.png"
            dictX[j] = fou
            j = j + 1

        dictFriends = dict()
        dictY = dict()
        j = 0
        k = 10000
        myFriends = fetch_friends(username)
        for f in myFriends:
            dictFriends[j] = f
            j = j + 1

            friendsLinks = fetch_my_links(f)
            for fl in friendsLinks:
                fou = dict()
                fou['link'] = fl
                if fl.endswith("jpg") or l.endswith("png") or l.endswith("gif"):
                    fou['image'] = fl
                else:
                    fou['image'] = "/static/diffsite_logo.png"
                dictY[k] = fou
                k = k + 1

        return render_template('home.html', username = username, dictX = dictX, dictY = dictY, dictFriends = dictFriends)

@app.route('/create', methods=['POST'])
def create():
    return render_template('create.html')

@app.route('/created', methods=['POST'])
def created():
    username = str(request.form['username'])
    password = str(request.form['password'])
    create_user(username, password)
    if not session.get('logged_in'):
        return create()
    return home()

@app.route('/linkpaste', methods=['POST'])
def linkpaste():
    link = str(request.form['linkpaste'])
    upload_link(link, session.get('username'))
    return home()

@app.route('/remove', methods=['POST'])
def remove():
    link = request.form.to_dict()
    link = next(iter(link))
    remove_link(link, session.get('username'))
    return home()

@app.route('/userpaste', methods=['POST'])
def userpaste():
    user = str(request.form['userpaste'])
    add_friend(session.get('username'), user)
    return home()

@app.route('/login', methods=['POST'])
def do_admin_login():

    username = str(request.form['username'])
    password = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['username'] = username
    else:
        print('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = 'none'
    return home()

if __name__ == "__main__":
    app.secret_key = '2435#$5@#45#$5345'
    app.run(host='0.0.0.0', debug=True)
