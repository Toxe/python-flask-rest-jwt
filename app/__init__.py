from flask import Flask
from config import Config
from app.db import Database
from flask_jwt_extended import JWTManager


db = Database()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


from app import models
