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
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

class Link(database):
    """"""
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    link = Column(String)
    username = Column(String)
    time = Column(DateTime)

    def __init__(self, link, username):
        """"""
        self.link = link
        self.username = username
        self.time = datetime.datetime.now()

class Friendship(database):
    """"""
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True)
    usernameA = Column(String)
    usernameB = Column(String)

    def __init__(self, usernameA, usernameB):
        """"""
        self.usernameA = usernameA
        self.usernameB = usernameB

class Pending_Friendship(database):
    """"""
    __tablename__ = "pending_friendships"

    id = Column(Integer, primary_key=True)
    usernameA = Column(String)
    usernameB = Column(String)

    def __init__(self, usernameA, usernameB):
        """"""
        self.usernameA = usernameA
        self.usernameB = usernameB

database.metadata.create_all(engine) # create tables
