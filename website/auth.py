from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def lougout():
    return "<p> lougout </p>"


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            flash("Please enter a username.", category="error")

        password = request.form.get("password")
        if not password:
            flash("Please enter a password.", category="error")

        if len(password) < 8:
            flash("Your password must be at least 8 characters long.",
                  category="error")

        confirmation = request.form.get("confirmation")

        if not confirmation:
            flash("You must confirm your password.", category="error")
        elif password != confirmation:
            flash("Passwords do not match", category="error")
        else:
            flash("Account created!", category="success")

    return render_template("register.html")
