from flask.helpers import url_for
from website.models import Candidate
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from .models import User, Poll, Candidate, ClosedPoll, ActivePoll, Room
from . import db


views = Blueprint('views', __name__)


@views.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)


@views.route("/create-poll", methods=["GET", "POST"])
@login_required
def create_poll():
    if request.method == "POST":
        num_candidates = request.form.get("num_candidates")

        if not num_candidates:
            flash("You must indicate the number of candidates.", category="error")
            return redirect(url_for("views.create_poll"))

        poll_name = request.form.get("poll_name")

        if not poll_name:
            flash("You must have a name for your poll.", category="error")
            return redirect(url_for("views.create_poll"))

        new_poll = Poll(user_id=current_user.id,
                        name=poll_name, status="active", num_candidates=num_candidates)

        db.session.add(new_poll)
        db.session.commit()

        return redirect(url_for("views.set_poll"))

    return render_template("create_poll.html", user=current_user)


@views.route("/set-poll", methods=["GET", "POST"])
@login_required
def set_poll():
    if request.method == "POST":
        return "Testing setting poll"

    return render_template("set_poll.html", user=current_user)
