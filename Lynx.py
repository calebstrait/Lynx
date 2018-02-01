# Lynx.py
# by Caleb Strait

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import session

echo = False;
engine = create_engine('sqlite:///lynx.db', echo=echo)
Session = sessionmaker(bind=engine)
s = Session()

def create_user(username, email, openid):
    import datetime
    from tabledef import User

    user = User(username,email,openid)
    s.add(user)
    s.commit()

def upload_link(url, title, username, board_ID):
    from tabledef import Link

    link = Link(url,title,username,board_ID)
    s.add(link)
    s.commit()

def remove_link(url, username, title, board_ID):
    from tabledef import Link

    query = s.query(Link).filter(Link.link == url, Link.title == title, Link.board_ID == board_ID)
    result = query.first()
    s.delete(result)
    s.commit()

def fetch_links(board_ID):
    from tabledef import Link

    query = s.query(Link).filter(Link.board_ID.in_([board_ID]))
    result = query.all()
    ret = list()
    for l in result:
        ret.append(l)
    return ret

def fetch_boards(username):
    from tabledef import Board_Permission, Board

    query = s.query(Board_Permission).filter(Board_Permission.username.in_([username]))
    bps = query.all()
    ret = list()
    for p in bps:
        query = s.query(Board).filter(Board.board_ID.in_([p.board_ID]))
        ret.append(query.first())
    return ret

def add_board_permission(username,board_ID):
    from tabledef import Board_Permission

    bp = Board_Permission(username,board_ID)
    s.add(bp)
    s.commit()

def remove_board_permission(username,board_ID):
    from tabledef import Board_Permission

    query = s.query(Board_Permission).filter(Board_Permission.username == username, Board_Permission.board_ID == board_ID)
    result = query.first()
    s.delete(result)
    s.commit()

def add_comment(content,username,board_ID,link_ID):
    from tabledef import Comment

    c = Comment(content,username,board_ID,link_ID)
    s.add(c)
    s.commit()

def remove_comment(comment_ID):
    from tabledef import Comment

    query = s.query(Comment).filter(Comment.id == comment_ID)
    result = query.first()
    s.delete(result)
    s.commit()

def fetch_comments(link):
    from tabledef import Link, Comment

    idn = link.id
    query = s.query(Comment).filter(Comment.link_ID.in_([idn]))
    qa = query.all()
    ret = list()
    for c in qa:
        ret.append(c)
    return ret
