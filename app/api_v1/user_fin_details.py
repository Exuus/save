from flask import request
from . import api
from .. import db
from ..models import User, UserFinDetails
from ..decorators import json, paginate, no_cache


@api.route('/fin-details/<int:id>', methods=['GET'])
@json
def get_fin_details(id):
    return UserFinDetails.query.get_or_404(id)


@api.route('/users/<int:id>/fin-details/', methods=['GET'])
@json
@paginate('fin_details')
def get_user_fin_details(id):
    user = User.query.get_or_404(id)
    return user.financial


@api.route('/users/<int:id>/fin-details/', methods=['POST'])
@json
def new_user_fin_details(id):
    users = User.query.get_or_404(id)
    fin_details = UserFinDetails(users=users)
    fin_details.import_data(request.json)
    db.session.add(fin_details)
    db.session.commit()
    return {}, 201, {'Location': fin_details.get_url()}


@api.route('/fin-details/<int:id>', methods=['PUT'])
@json
def edit_fin_details(id):
    fin_details = UserFinDetails.query.get_or_404(id)
    fin_details.import_data(request.json)
    db.session.add(fin_details)
    db.session.commit()
    return {}