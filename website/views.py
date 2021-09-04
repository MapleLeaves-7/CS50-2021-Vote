from flask.helpers import url_for
from website.models import Candidate
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from .models import Poll, Candidate, ClosedPoll
from . import db
from random import sample
import string


views = Blueprint('views', __name__)

ALL = string.ascii_letters + string.digits
ROOMKEY_LENGTH = 12


@views.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        roomkey = request.form.get("roomkey")

        if not roomkey:
            flash("Please enter a room key.", category="error")
            return render_template("index.html")

        return redirect(url_for("views.vote", roomkey=roomkey))
    return render_template("index.html")


@views.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html", user=current_user)


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

        while True:
            # Generate roomkey
            roomkey = "".join(sample(ALL, ROOMKEY_LENGTH))
            print(roomkey)

            # Check that roomkey does not already exist
            current_room_keys = db.session.query(
                Poll).filter_by(roomkey=roomkey).all()

            if not current_room_keys:
                break

        # If not, add this poll to the database
        new_poll = Poll(user_id=current_user.id,
                        name=poll_name, roomkey=roomkey, status="active", num_candidates=num_candidates)

        db.session.add(new_poll)
        db.session.commit()

        # Get the current poll just created
        current_poll = db.session.query(Poll).filter(
            Poll.user_id == current_user.id).filter(Poll.name == poll_name).first()

        return redirect(url_for("views.set_poll", roomkey=current_poll.roomkey))

    return render_template("create_poll.html", user=current_user)


@views.route("/set-poll/<roomkey>", methods=["GET", "POST"])
@login_required
def set_poll(roomkey):
    # Get the number of candidates for this poll
    current_poll = db.session.query(Poll).filter(
        Poll.user_id == current_user.id).filter(Poll.roomkey == roomkey).first()

    num_candidates = current_poll.num_candidates

    if request.method == "POST":
        # Create an array of candidates
        candidates = []
        for i in range(num_candidates):
            candidate = request.form.get(f"candidate{i}")
            if not candidate:
                flash("Must fill in names of all the candidates", category="error")
                return redirect(url_for("views.set_poll", roomkey=current_poll.roomkey))
            elif len(candidate) > 150:
                flash("Name of candidate must be less than 150 characters.",
                      category="error")
                return redirect(url_for("views.set_poll", roomkey=current_poll.roomkey))

            candidates.append(candidate)

        if len(set(candidates)) != num_candidates:
            flash("Candidate names must be unique.", category="error")
            return redirect(url_for("views.set_poll", roomkey=current_poll.roomkey))

        # Iternate through array of candidate names and add candidate to database
        for candidate in candidates:
            new_candidate = Candidate(
                poll_id=current_poll.id, name=candidate, roomkey=roomkey, votes=0)
            db.session.add(new_candidate)
            db.session.commit()

        flash("Poll created!", category="success")
        return redirect(url_for("views.homepage"))

    else:
        return render_template("set_poll.html", user=current_user, num_candidates=num_candidates, roomkey=roomkey)


@views.route("/vote/<roomkey>", methods=["GET", "POST"])
def vote(roomkey):
    # Array of candidate objects
    candidates = db.session.query(Candidate).filter(
        Candidate.roomkey == roomkey).all()

    if request.method == "GET":
        # Check if there are any closed polls with this roomkey
        closed_polls = db.session.query(Poll).filter_by(
            roomkey=roomkey).filter_by(status="closed").all()

        # Redirect them to the index page if there are
        if closed_polls:
            flash("This poll has already been closed", category="error")
            return redirect(url_for("views.index"))

        return render_template("vote.html", candidates=candidates, roomkey=roomkey)
    else:
        # Get the value of the candidate whose checkbox was checked
        # In this case, I set the value to be the candidate's id
        current_candidate_id = request.form.get("candidate")

        # Get the candidate object from the database
        current_candiate = db.session.query(
            Candidate).get(current_candidate_id)
        print(current_candiate)

        # Increment the number of votes they have by 1
        current_candiate.votes += 1

        current_poll = db.session.query(
            Poll).filter_by(roomkey=roomkey).first()

        current_poll.num_votes += 1

        db.session.commit()
        flash("Thank you for voting!", category="success")
        return redirect(url_for("views.index"))


@views.route("/active-polls")
@login_required
def active_polls():
    # Array of polls objects the user currently has
    polls = db.session.query(Poll).filter(
        Poll.user_id == current_user.id).filter(Poll.status == "active").all()

    return render_template("active_polls.html", user=current_user, polls=polls)


@views.route("/closed-polls", methods=["GET", "POST"])
@login_required
def closed_polls():
    if request.method == "POST":
        poll_id = request.form.get("poll")

        current_poll = db.session.query(
            Poll).filter(Poll.id == poll_id).first()

        current_poll.status = "closed"

        candidates = db.session.query(Candidate).filter(
            Candidate.poll_id == poll_id).all()

        # Sort the candidates in descending order of number of votes
        candidates.sort(key=lambda candidate: candidate.votes, reverse=True)

        max_vote = candidates[0].votes

        # Filters the list to get only candidates with the maximum number of votes
        # Then uses map to convert candidate object into only the candidate's name
        # Then converts that into a list instead of a map object
        winning_candidate = list(map(lambda candidate: candidate.name, filter(
            lambda candidate: True if candidate.votes == max_vote else False, candidates)))

        print(winning_candidate)

        if len(winning_candidate) > 1:
            winners = ", ".join(winning_candidate)
            new_closed_poll = ClosedPoll(poll_id=poll_id, winner=winners)
        else:
            winner = winning_candidate[0]
            new_closed_poll = ClosedPoll(poll_id=poll_id, winner=winner)

        db.session.add(new_closed_poll)

        db.session.commit()

    closed_polls = db.session.query(Poll, ClosedPoll).filter(
        Poll.id == ClosedPoll.poll_id).filter(Poll.user_id == current_user.id).all()

    return render_template("closed_polls.html", user=current_user, closed_polls=closed_polls)


@views.route("/current-poll/<roomkey>", methods=["GET", "POST"])
@login_required
def current_poll(roomkey):
    candidates = db.session.query(Candidate).filter_by(roomkey=roomkey).all()

    poll = db.session.query(Poll).filter_by(roomkey=roomkey).first()

    closed_poll = db.session.query(
        ClosedPoll).filter_by(poll_id=poll.id).first()

    return render_template("current_poll.html", user=current_user, candidates=candidates, poll=poll, closed_poll=closed_poll)
