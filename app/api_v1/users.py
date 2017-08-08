from flask import request
from . import api
from .. import db
from ..models import User, Organization
from ..decorators import json, paginate, no_cache


@api.route('/users/', methods=['GET'])
@no_cache
@json
@paginate('users')
def get_users():
    return User.query


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return User.query.get_or_404(id)


@api.route('/organization/<int:id>/users/', methods=['POST'])
def new_user(id):
    organization = Organization.query.get_or_404(id)
    user = User(organization=organization)
    user.import_data(request.json)
    user.set_password(request.json['password'])
    db.session.add(user)
    db.session.commit()
    return {}, 201, {'Location': user.get_url()}

