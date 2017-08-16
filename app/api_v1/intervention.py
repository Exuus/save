from flask import request
from . import api
from .. import db
from ..models import InterventionArea, Village, Project, User
from ..decorators import json, paginate, no_cache


@api.route('/interventions/<int:id>', methods=['GET'])
@json
def get_intervention_area(id):
    return InterventionArea.query.get_or_404(id)


@api.route('/projects/<int:id>/interventions/', methods=['GET'])
@json
@paginate('intervention_area')
def get_project_intervention_area(id):
    project = Project.query.get_or_404(id)
    return project.intervention


@api.route('/agents/<int:id>/projects/interventions/', methods=['GET'])
@json
@paginate('agent_project')
def get_agent_project(id):
    user = User.query.get_or_404(id)
    return user.intervention


@api.route('/projects/<int:id>/intervention/', methods=['POST'])
@json
def new_intervention(id):
    project = Project.query.get_or_404(id)
    intervention = InterventionArea(project=project)
    intervention.import_data(request.json)
    db.session.add(intervention)
    db.session.commit()

    return {}, 201, {'Location': intervention.get_url()}


@api.route('/interventions/<int:id>')
@json
def edit_invention(id):
    intervention = InterventionArea.query.get_or_404(id)
    intervention.import_data(request.json)
    db.session.add(intervention)
    db.session.commit()
    return {}