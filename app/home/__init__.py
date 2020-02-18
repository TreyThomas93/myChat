from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from extensions import socketio, db
from models import Users, Messages
from flask_socketio import send, emit, disconnect
import functools
import pytz
from datetime import datetime

home = Blueprint("home", __name__, template_folder="templates", static_folder="static", static_url_path="/home/static")

@home.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        return render_template("home/index.html", user=current_user)

    return redirect(url_for("authorize.login"))

## SOCKETIO ##

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on("connect user")
@authenticated_only
def connect_handler(json):
    """
    If user is logged in and authenticated, then broadcast to all clients
    :param: None
    :return: None/False
    """
    dt = json["datetime"]
    if current_user.is_authenticated:
        msg = "has joined the chat"
        emit("on connect", {"user" : current_user.username, "message" : msg, "dt" : dt}, broadcast=True)
    else:
        return False

@socketio.on("message")
@authenticated_only
def message_handler(json):
    """
    Receives message and broadcasts it to all
    :param json: dict
    :return: None
    """
    msg = json["message"]
    dt = json["datetime"]
    print(f"[NEW MESSAGE]: {msg} - {dt}")
    
    ## save message to database ##
    add = Messages(message=msg, message_date=dt, messenger=current_user)
    db.session.add(add)
    db.session.commit()

    ## broadcast ##
    # msg = f"{current_user.username}: {msg} - {dt}"
    # send(msg, broadcast=True)

    emit("receive message", {"user" : current_user.username, "message" : msg, "dt" : dt}, broadcast=True)