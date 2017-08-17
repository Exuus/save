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


@api.route('/organizations/<int:id>/agents/', methods=['GET'])
@json
@paginate('agents')
def get_organization_agents(id):
    organization = Organization.query.get_or_404(id)
    return organization.users.filter_by(type=2)


@api.route('/organizations/<int:id>/members/', methods=['GET'])
@json
@paginate('members')
def get_organization_members(id):
    organization = Organization.query.get_or_404(id)
    return organization.users.filter_by(type=3)


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


@api.route('/login/', methods=['POST'])
@json
def user_login():
    data = request.json
    user = User.query.\
        filter((User.email == data['username']) | (User.phone == data['username']) | (User.username == data['username'])).\
        first()
    if user.verify_password(data['password']):
        return user
    return {}, 404


@api.route('/users/confirmation/', methods=['POST'])
@json
def user_confirmation_code():
    data = request.json
    user = User.query.\
        filter(User.email == data['email'], User.confirmation_code == data['code']).\
        first()
    if user:
        return user
    return {}, 404


@api.route('/users/<int:id>', methods=['PUT'])
@json
def edit_users(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return {}

