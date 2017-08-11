from flask import request
from . import api
from .. import db
from ..models import InterventionArea, Village, Project, User
from ..decorators import json, paginate, no_cache


@api.route('/interventions/<int:id>', methods=['GET'])
@json
def get_intervention_area(id):
    return InterventionArea.query.get_or_404(id)


@api.route('/projects/<int:id>/intervention/', methods=['GET'])
@json
@paginate('intervention_area')
def get_project_intervention_area(id):
    project = Project.query.get_or_404(id)
    return project.intervention


@api.route('/project/<int:id>/user/<int:user_id>/intervention', methods=['POST'])
@json
def new_intervention(id, user_id):
    project = Project.query.get_or_404(id)
    user = User.query.get_or_404(user_id)
    intervention = InterventionArea(project=project, user=user)
    intervention.import_data(request.json)
    db.session.add(intervention)
    db.session.commit()

    return {}, 201, {'Location': intervention.get_url()}