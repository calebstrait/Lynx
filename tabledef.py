from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import datetime

engine = create_engine('sqlite:///lynx.db', echo=False)
database = declarative_base()

class User(database):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(60))
    email = Column(String(200))
    id_num = Column(String(200))

    def __init__(self, username, email, id_num):
        """"""
        self.username = username
        self.email = email
        self.id_num = id_num

class Link(database):
    """"""
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    link = Column(String)
    title = Column(String)
    username = Column(String)
    time = Column(DateTime)
    board_ID = Column(Integer)

    def __init__(self, link, title, username, board_ID):
        """"""
        self.link = link
        self.title = title
        self.username = username
        self.time = datetime.datetime.now()
        self.board_ID = board_ID

class Board(database):
    """"""
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    creator = Column(String)
    title = Column(String)
    board_ID = Column(String)

    def __init__(self, creator, title, board_ID):
        """"""
        self.creator = creator
        self.title = title
        self.board_ID = board_ID

class Board_Permission(database):
    """"""
    __tablename__ = "board_permissions"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    board_ID = Column(Integer)

    def __init__(self, username, board_ID):
        """"""
        self.username = username
        self.board_ID = board_ID

class Comment(database):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    username = Column(String)
    time = Column(DateTime)
    board_ID = Column(Integer)
    link_ID = Column(Integer)

    def __init__(self, content, username, board_ID, link_ID):
        self.content = content
        self.username = username
        self.time = datetime.datetime.now()
        self.board_ID = board_ID
        self.link_ID = link_ID

database.metadata.create_all(engine) # create tables
