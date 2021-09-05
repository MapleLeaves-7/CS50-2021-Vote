from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    # polls = db.relationship("Poll")


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    roomkey = db.Column(db.String)
    name = db.Column(db.String(150))
    votes = db.Column(db.Integer)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    status = db.Column(db.String(6))
    roomkey = db.Column(db.String(18), unique=True)
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    num_candidates = db.Column(db.Integer)
    num_votes = db.Column(db.Integer, default=0)
    # candidates = db.relationship("Candidate")


class ClosedPoll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), unique=True)
    winner = db.Column(db.String)
    time_closed = db.Column(db.DateTime(timezone=True), default=func.now())
