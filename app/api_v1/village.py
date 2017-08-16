from flask import request
from . import api
from .. import db
from ..models import Village
from ..decorators import json, paginate, no_cache


@api.route('/villages/', methods=['GET'])
@no_cache
@json
@paginate('villages')
def get_villages():
    return Village.query


@api.route('/villages/<int:id>', methods=['GET'])
@json
def get_village(id):
    return Village.query.get_or_404(id)


@api.route('/villages/', methods=['POST'])
@json
def new_village():
    village = Village()
    village.import_data(request.json)
    db.session.add(village)
    db.session.commit()
    return {}, 201, {'Location': village.get_url()}


