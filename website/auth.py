from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return "<p> login </p>"


@auth.route("/logout")
def lougout():
    return "<p> lougout </p>"


@auth.route("/register")
def register():
    return "<p> register</p>"
