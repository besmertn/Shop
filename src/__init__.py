from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config


global_products = []
global_products_json = []
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)

    from .main import bp as main_bp
    from .auth import bp as auth_bp
    from .shipment import bp as shipment_bp
    from .products import bp as products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shipment_bp, url_prefix='/shipment')
    app.register_blueprint(shipment_bp, url_prefix='/shipment')
    app.register_blueprint(products_bp, url_prefix='/products')

    return app
