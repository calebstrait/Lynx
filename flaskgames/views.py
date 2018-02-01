from flask import Flask, flash, redirect, render_template, request, session, abort
from flaskgames import app
import os
from Lynx import *
from sqlalchemy.orm import sessionmaker
from tabledef import *
import pytz

engine = create_engine('sqlite:///lynx.db', echo=False)
Session = sessionmaker(bind=engine)
s = Session()

@app.route('/after_login', methods=['GET', 'POST'])
def after_login():
    from google.oauth2 import id_token
    from google.auth.transport import requests
    token = request.args.get('id_token')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '885982122839-ogpamdsmq6jij7j3tphc40cr9cqco7o6.apps.googleusercontent.com')
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        id_num = idinfo['sub']
    except ValueError:
        return render_template('login.html') # Invalid token
    session['id_num'] = id_num
    user = s.query(User).filter(User.id_num.in_([id_num])).first()
    if user is not None:
        session['username'] = user.username
        session['logged_in'] = True
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/created', methods=['GET', 'POST'])
def created():
    username = str(request.form['username'])
    id_num = session.get('id_num')
    user = s.query(User).filter(User.username.in_([username])).first()
    if user is None:
        create_user(username, session.get('email'), id_num)
        session['username'] = username
        session['logged_in'] = True
        return redirect('/')
    else:
        return render_template('create.html') #username taken

@app.route('/')
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = session.get('username')

        dictBoards = dict()
        datetime_dict = dict()
        dictComments = dict()
        myBoards = fetch_boards(username)
        d = 0
        for b in myBoards:
            sub = dict()
            sub['title'] = b.title
            sub['board_ID'] = b.board_ID
            dictBoards[d] = sub
            d = d + 1
            board_links = fetch_links(b.board_ID)
            for bl in board_links:
                subX = dict()
                subX['link'] = bl.link
                subX['ltitle'] = bl.title
                subX['board_title'] = b.title
                subX['board_ID'] = b.board_ID
                subX['link_ID'] = bl.id
                if username == bl.username:
                    subX['yours'] = 1
                else:
                    subX['yours'] = 0
                subX['creator'] = bl.username
                datetime_dict[bl.time] = subX

                comments = fetch_comments(bl)
                subXX = dict()
                for c in comments:
                    subXXX = dict()
                    subXXX['content'] = c.content
                    subXXX['username'] = c.username
                    subXXX['comment_ID'] = c.id
                    dt = pytz.utc.localize(c.time).astimezone(pytz.timezone('EST'))
                    subXXX['time'] = dt.strftime("%b %-d, %Y  %-I:%M %p")
                    subXX[c.time] = subXXX
                sortedSubXX = dict()
                j = 0
                for key, value in sorted(subXX.items()):
                    sortedSubXX[j] = value
                    j = j + 1
                dictComments[bl.id] = sortedSubXX

        dictLinks = dict()
        j = 0
        for key, value in sorted(datetime_dict.items()):
            dictLinks[j] = value
            j = j + 1

        return render_template('home.html', username = username, dictLinks = dictLinks, dictBoards = dictBoards, dictBoardsEmpty = (len(dictBoards) == 0), dictComments = dictComments)

@app.route('/linkpaste', methods=['POST'])
def linkpaste():
    link = str(request.form['linkpaste'])
    title = str(request.form['linktitle'])
    board_ID = str(request.form['board_ID'])
    upload_link(link, title, session.get('username'), board_ID)
    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove():
    link = str(request.form['link'])
    title = str(request.form['title'])
    board_ID = str(request.form['board_ID'])
    remove_link(link, session.get('username'), title, board_ID)
    return redirect('/')

@app.route('/boardpaste', methods=['GET','POST'])
def boardpaste():
    board_ID = str(request.form['boardpaste'])
    add_board_permission(session.get('username'), board_ID)
    return redirect('/')

@app.route('/unsub', methods=['GET','POST'])
def unsub():
    board_ID = request.args.get('b', type = str)
    remove_board_permission(session.get('username'), board_ID)
    return redirect('/')

@app.route('/boardcreate', methods=['GET','POST'])
def boardcreate():
    import uuid
    username = session.get('username')
    title = str(request.form['boardcreate'])
    uuidX = str(uuid.uuid1())
    board_ID = uuidX.replace("-", "")
    board = Board(username,title,board_ID)
    s.add(board)
    s.commit()
    add_board_permission(username,board_ID)
    return redirect('/')

@app.route('/commentAdd', methods=['GET','POST'])
def commentAdd():
    content = str(request.form['comment_content'])
    username = session.get('username')
    board_ID = str(request.form['board_ID'])
    link_ID = str(request.form['link_ID'])
    add_comment(content,username,board_ID,link_ID)
    return redirect('/')

@app.route('/commentRemove', methods=['POST'])
def commentRemove():
    comment_ID = str(request.form['comment_ID'])
    remove_comment(comment_ID)
    return redirect('/')

@app.route('/logout')
def logout():
    session['id_num'] = None
    session['logged_in'] = False
    session['username'] = None
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = '2435#$5@#45#$5345'
    app.run(host='0.0.0.0', debug=True)
