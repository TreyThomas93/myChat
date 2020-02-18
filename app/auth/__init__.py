from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from extensions import socketio, login_manager, db
from models import Users
from flask_socketio import send, emit
import functools

authorize = Blueprint("authorize", __name__, template_folder="templates", static_folder="static", static_url_path="/auth/static")

login_manager.login_view = "authorize.login"
login_manager.login_message = "You Must Be Logged In To Access!"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    """
    sets current user object
    :return: user object
    """
    return Users.query.get(user_id)

## LOGIN/LOGOUT ##
@authorize.route("/login", methods=["GET", "POST"])
def login():
    """
    logs in users.
    :return: template
    """
    if request.method == "POST":
        username = request.form["username"]
        if username:
            user = Users.query.filter_by(username=username).first()
            if user:
                login_user(user)
                ## add to login count
                user.login_count+=1
                db.session.commit()
                
                return redirect(url_for("home.index"))
            else:
                flash("Username does not exist!", "warning")
        else:
                flash("Invalid Username!", "warning")

    return render_template("auth/login.html")

@authorize.route("/logout")
def logout():
    """
    logs out user.
    :return: template
    """
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for("authorize.login"))

## REGISTER ##
@authorize.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        if username:
            exists = Users.query.filter_by(username=username).first()
            if not exists: # if username not in database, then add new user
                add = Users(username=username)
                db.session.add(add)
                db.session.commit()

                flash("Thanks for registering! Please login!", "success")
                return redirect(url_for("authorize.login"))

            else: # if username already exists, alert the user
                flash("Username already exists!", "warning")

        else: # if username already exists, alert the user
                flash("Invalid Username!", "warning")   

    return render_template("auth/register.html")
