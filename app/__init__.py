# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail

# local imports
from config import app_config

# variable initialization
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    cors = CORS(app)
    migrate = Migrate(app, db)

    from app import model
    from .api_v1 import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/v1/users')

    # temporary route
    @app.route('/')
    def hello_world():
        return 'Hello World'

    return app



