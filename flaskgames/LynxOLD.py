# Lynx.py
# by Caleb Strait

echo = False;
def create_user(username, password):
    import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from tabledef import User
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    user = User(username,password)
    query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]))
    result = query.first()
    if result:
        print('that username is taken')
    else:
        s.add(user)
        s.commit()
        session['logged_in'] = True
        session['username'] = username

def upload_link(url, username):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from tabledef import Link
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    link = Link(url,username)
    s.add(link)
    s.commit()

def remove_link(url,username,title):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from tabledef import Link
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Link).filter(Link.username.in_([username]), Link.link.in_([url]),Link.username.in_([username]))
    result = query.first()
    s.delete(result)
    s.commit()

def fetch_my_links(username):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from tabledef import Link
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(Link).filter(Link.username.in_([username]))
    result = query.all()
    ret = list()
    for l in result:
        ret.append(l.link)
    return ret

def fetch_friends(username):
    from sqlalchemy import create_engine, or_
    from sqlalchemy.orm import sessionmaker
    from tabledef import Friendship
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(Friendship).filter(or_(Friendship.usernameA.in_([username]), Friendship.usernameB.in_([username])))
    result = query.all()
    ret = list()
    for f in result:
        if f.usernameA == username:
            ret.append(f.usernameB)
        else:
            ret.append(f.usernameA)
    return ret

def add_friendship(usernameA,usernameB):
    from sqlalchemy import create_engine, or_
    from sqlalchemy.orm import sessionmaker
    from tabledef import Friendship
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    friendship = Friendship(usernameA,usernameB)
    s.add(friendship)
    s.commit()

def add_friend(usernameA,usernameB):
    from sqlalchemy import create_engine, or_
    from sqlalchemy.orm import sessionmaker
    from tabledef import Pending_Friendship
    from flask import session

    engine = create_engine('sqlite:///lynx.db', echo=echo)
    Session = sessionmaker(bind=engine)
    s = Session()

    pending_friendship = Pending_Friendship(usernameA,usernameB)
    s.add(pending_friendship)
    s.commit()

    query = s.query(Pending_Friendship).filter(Pending_Friendship.usernameA.in_([usernameB]), Pending_Friendship.usernameB.in_([usernameA]))
    result = query.all()

    if result: # usernameB has pending friendship with usernameA
        add_friendship(usernameA,usernameB)
