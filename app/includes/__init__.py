from flask import Blueprint, render_template

includes = Blueprint("includes", __name__, template_folder="templates", static_folder="static", static_url_path="/includes/static")
