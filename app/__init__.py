# third-party imports
from flask import Flask, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from .decorators import json, no_cache, rate_limit
from .errorhandlers import bad_request, forbidden, not_found, method_not_supported

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

    from app import models
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    # register errors handlers

    app.register_error_handler(400, bad_request)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_supported)

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    # authentication token route
    from .auth import auth

    @app.route('/get-auth-token')
    @auth.login_required
    @rate_limit(1, 600)  # one call per 10 minute period
    @no_cache
    @json
    def get_auth_token():
        return {'token': g.user.generate_auth_token()}


    return app




