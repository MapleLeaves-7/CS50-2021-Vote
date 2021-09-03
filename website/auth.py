from flask import Blueprint
from flask.templating import render_template

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return "<p> login </p>"


@auth.route("/logout")
def lougout():
    return "<p> lougout </p>"


@auth.route("/register")
def register():
    return render_template("register.html")
