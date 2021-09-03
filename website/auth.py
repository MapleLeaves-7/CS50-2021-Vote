from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.session.query(User).filter(User.username == username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect password. Try again.", category="error")
        else:
            flash("User does not exist.", category="error")

    return render_template("login.html")


@auth.route("/logout")
def lougout():
    return "<p> lougout </p>"


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Please enter a username.", category="error")
            return render_template("register.html")

        user = User.query.filter_by(username=username).first()

        if user:
            flash("User already exists.", category="error")
        elif not password:
            flash("Please enter a password.", category="error")
        # elif len(password) < 8:
        #     flash("Your password must be at least 8 characters long.",
        #           category="error")
        elif not confirmation:
            flash("You must confirm your password.", category="error")
        elif password != confirmation:
            flash("Passwords do not match", category="error")
        else:
            new_user = User(username=username, password=generate_password_hash(
                password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect(url_for("views.index"))

    return render_template("register.html")
