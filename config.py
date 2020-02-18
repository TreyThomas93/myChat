import os
import sqlite3

SECRET_KEY = os.urandom(20) 

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getcwd()}/myChat.db"
SQLALCHEMY_BINDS = ({"Messages" : f"sqlite:///{os.getcwd()}/myChat.db"})

DEBUG = True