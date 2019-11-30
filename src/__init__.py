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

    from .users.routes import bp as users_bp

    app.register_blueprint(users_bp, url_prefix='/api')

    return app
