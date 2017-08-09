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
@json
def get_user(id):
    return User.query.get_or_404(id)


@api.route('/organizations/<int:id>/users/', methods=['GET'])
@json
@paginate('users')
def get_organization_users(id):
    organization = Organization.query.get_or_404(id)
    return organization.users


@api.route('/organizations/<int:id>/users/', methods=['POST'])
@json
def new_user(id):
    organization = Organization.query.get_or_404(id)
    user = User(organization=organization)
    user.import_data(request.json)
    user.set_password(request.json['password'])
    db.session.add(user)
    db.session.commit()
    return {}, 201, {'Location': user.get_url()}

