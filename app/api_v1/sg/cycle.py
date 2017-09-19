from flask import request
from .. import api
from ... import db
from ...models import SavingGroupCycle, SavingGroup
from ...decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError


@api.route('/cycle/<int:id>', methods=['GET'])
@json
def get_cycle(id):
    return SavingGroupCycle.query.get_or_404(id)


@api.route('/sg/<int:id>/cycle/', methods=['GET'])
@no_cache
@json
@paginate('cycles')
def get_sg_cycle(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return saving_group.sg_cycle


@api.route('/sg/<int:id>/cycle/', methods=['POST'])
@json
def new_sg_cycle(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle(saving_group=saving_group)
    cycle.import_data(request.json)
    try:
        db.session.add(cycle)
        db.session.commit()
        return {}, 201, {'Location': cycle.get_url()}
    except IntegrityError:
        db.session.rollback()
        return {}, 500