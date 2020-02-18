from flask import Flask, Blueprint
from extensions import socketio, login_manager, db
import os

## INIT APP ##
app = Flask(__name__, template_folder=None, static_folder=None)

## INIT CONFIG FILE ##
app.config.from_pyfile(f"{os.getcwd()}/config.py")

## INIT EXTENSIONS ##
socketio.init_app(app)
login_manager.init_app(app)
db.init_app(app)

## IMPORT BLUEPRINTS AND REGISTER THEM ##
from .includes import includes
from .auth import authorize
from .home import home
from .history import history

app.register_blueprint(includes)
app.register_blueprint(authorize)
app.register_blueprint(home)
app.register_blueprint(history)

