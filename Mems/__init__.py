from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    from .models import Mems
    from .routes import main_routes

    app.register_blueprint(main_routes)

    return app
