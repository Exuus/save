from flask import request
from . import api
from .. import db
from ..models import Organization
from ..decorators import json, paginate, no_cache


@api.route('/organizations/', methods=['GET'])
@json
@no_cache
@paginate('organizations')
def get_organizations():
    return Organization.query


@api.route('/organizations/<int:id>', methods=['GET'])
@json
def get_organization(id):
    return Organization.query.get_or_404(id)


@api.route('/organizations/', methods=['POST'])
@json
def new_organization():
    organization = Organization()
    organization.import_data(request.json)
    db.session.add(organization)
    db.session.commit()
    return {}, 201, {'Location': organization.get_url()}


@api.route('/organizations/<int:id>', methods=['PUT'])
@json
def edit_organization(id):
    organization = Organization.query.get_or_404(id)
    organization.import_data(request.json)
    db.session.add(organization)
    db.session.commit()
    return {}