from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
