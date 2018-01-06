from flask import request
from . import api
from .. import db
from ..models import InterventionArea, Project, ProjectAgent, AgentInterventionArea
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


@api.route('/projects/<int:id>/intervention/', methods=['POST'])
@json
def new_intervention(id):
    for area in request.json:
        project = Project.query.get_or_404(id)
        intervention = InterventionArea(project=project)
        intervention.import_data(area)
        db.session.add(intervention)
        db.session.commit()

    return {}, 201, {'Location': intervention.get_url()}


@api.route('/interventions/<int:id>', methods=['PUT'])
@json
def edit_invention(id):
    intervention = InterventionArea.query.get_or_404(id)
    intervention.import_data(request.json)
    db.session.add(intervention)
    db.session.commit()
    return {}


@api.route('/project-agent/<int:id>/intervention-area/', methods=['POST'])
@json
def new_project_agent_intervention_area(id):
    for area in request.json:
        project_agent = ProjectAgent.query.get_or_404(id)
        agent_intervention = AgentInterventionArea(project_agent=project_agent)
        agent_intervention.import_data(area)
        db.session.add(agent_intervention)
        db.session.commit()

    return {}, 201
