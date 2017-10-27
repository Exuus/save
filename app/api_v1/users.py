from flask import request, jsonify
from . import api
from .. import db
from ..models import User, Organization, SavingGroupMember
from ..decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError
from ..errorhandlers import internal_server_error
from ..save_sms import save_sms


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


@api.route('/users/members/<phone>')
@json
def get_users_members(phone):
    user = User.query.\
        filter(User.phone == phone).\
        filter_by(type=3).first()
    if user:
        return SavingGroupMember.query.\
            filter(SavingGroupMember.user_id == user.id).first()
    return {}, 404


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
    try:
        db.session.add(user)
        db.session.commit()

        if request.json['type'] == 3:
            save_sms(request.json['phone'], user.confirmation_code)

        return user
    except IntegrityError:
        db.session.rollback()
        return internal_server_error()


@api.route('/login/', methods=['POST'])
@json
def user_login():
    data = request.json
    user = User.query.\
        filter((User.email == data['username']) | (User.phone == data['username']) | (User.username == data['username'])).\
        first()
    if user:
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


@api.route('/users/sms/', methods=['POST'])
def send_message():
    save_sms(250785383100, 'sms text')
    return jsonify(True)

