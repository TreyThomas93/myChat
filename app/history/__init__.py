from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from extensions import db
from models import Messages

history = Blueprint("history", __name__, template_folder="templates", static_folder="static", static_url_path="/history/static")

@history.route("/history")
@login_required
def user_history():
    messages = Messages.query.filter_by(messenger=current_user).all()
    return render_template("history/history.html", messages=messages)