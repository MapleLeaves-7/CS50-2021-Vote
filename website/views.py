from flask import Blueprint
from flask.templating import render_template

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template("layout.html")
