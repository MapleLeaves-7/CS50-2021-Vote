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
        poll_name = request.form.get("poll_name")
        num_candidates = request.form.get("num_candidates")
        if not poll_name:
            flash("You must have a name for your poll.", category="error")
            return redirect(url_for("views.create_poll"))
        elif not num_candidates:
            flash("You must indicate the number of candidates.", category="error")
            return redirect(url_for("views.create_poll"))

        # Checking if this user already has a poll of the same name
        current_poll_names = db.session.query(Poll).filter(
            Poll.user_id == current_user.id).filter(Poll.name == poll_name).all()

        if current_poll_names:
            flash("You already have a poll of that name.", category="error")
            return redirect(url_for("views.create_poll"))

        # If not, add this poll to the database
        new_poll = Poll(user_id=current_user.id,
                        name=poll_name, status="active", num_candidates=num_candidates)

        db.session.add(new_poll)
        db.session.commit()

        # Get the current poll just created
        current_poll = db.session.query(Poll).filter(
            Poll.user_id == current_user.id).filter(Poll.name == poll_name).first()

        return redirect(url_for("views.set_poll", poll_id=current_poll.id))

    return render_template("create_poll.html", user=current_user)


@views.route("/set-poll/<poll_id>", methods=["GET", "POST"])
@login_required
def set_poll(poll_id):
    # Get the number of candidates for this poll
    current_poll = db.session.query(Poll).filter(
        Poll.user_id == current_user.id).filter(Poll.id == poll_id).first()

    num_candidates = current_poll.num_candidates

    if request.method == "POST":
        candidates = []
        for i in range(num_candidates):
            candidate = request.form.get(f"candidate{i}")
            if not candidate:
                flash("Must fill in names of all the candidates", category="error")
                return redirect(url_for("views.set_poll", poll_id=current_poll.id))
            elif len(candidate) > 150:
                flash("Name of candidate must be less than 150 characters.",
                      category="error")
                return redirect(url_for("views.set_poll", poll_id=current_poll.id))

            candidates.append(candidate)

        if len(set(candidates)) != num_candidates:
            flash("Candidate names must be unique.", category="error")
            return redirect(url_for("views.set_poll", poll_id=current_poll.id))

        for candidate in candidates:
            new_candidate = Candidate(
                poll_id=current_poll.id, name=candidate, votes=0)
            db.session.add(new_candidate)
            db.session.commit()

        flash("Poll created!", category="success")
        return redirect(url_for("views.index"))

    else:
        return render_template("set_poll.html", user=current_user, num_candidates=num_candidates, poll_id=current_poll.id)
