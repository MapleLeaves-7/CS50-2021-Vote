from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from os import path
from flask_login import LoginManager

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

db = SQLAlchemy()

# DB_NAME = "voting.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "asdfasdfasdf asdfasdfasdf"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://erocdveylmflpx:630e2dacaaeb5e219958ca997f25b5f197ce2eb3503076c2a3ca4f75a1c861fb@ec2-34-193-113-223.compute-1.amazonaws.com:5432/d9gfi6r0ojd0e7"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.index"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print("Created Database!")
