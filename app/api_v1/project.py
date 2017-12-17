from flask import request
from . import api
from .. import db
from ..models import Project, Organization, User, ProjectAgent, ProjectPartner, SavingGroup
from ..decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError


@api.route('/projects/<int:id>', methods=['GET'])
@json
def get_project(id):
    return Project.query.get_or_404(id)


@api.route('/organizations/<int:id>/projects/', methods=['GET'])
@no_cache
@json
@paginate('projects')
def get_organization_projects(id):
    organization = Organization.query.get_or_404(id)
    return organization.project


@api.route('/users/<int:id>/projects/', methods=['GET'])
@no_cache
@json
@paginate('projects')
def get_users_projects(id):
    user = User.query.get_or_404(id)
    return user.project_agent


@api.route('/project_agent/<int:id>')
@json
def get_project_agent(id):
    project_agent = ProjectAgent.query.get_or_404(id)
    return project_agent


@api.route('/agent/<int:id>/projects/', methods=['GET'])
@no_cache
@json
@paginate('projects')
def get_agent_projects(id):
    user = User.query.get_or_404(id)
    return user.project_agent


@api.route('/organizations/<int:id>/projects/', methods=['POST'])
@json
def new_project(id):
    organization = Organization.query.get_or_404(id)
    project = Project(organization=organization)
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return project, 201, {'Location': project.get_url()}


@api.route('/project/<int:id>/agents/', methods=['POST'])
@json
def new_project_agent(id):
    project = Project.query.get_or_404(id)
    project_agent = ProjectAgent(project=project)
    project_agent.import_data(request.json)
    try:
        db.session.add(project_agent)
        db.session.commit()
    except IntegrityError:
        db.session().rollback()
        return {}, 500
    return {}, 201, {'Location': project_agent.get_url()}


@api.route('/projects/<int:id>', methods=['PUT'])
@json
def edit_project(id):
    project = Project.query.get_or_404(id)
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return {}


@api.route('/projects/<int:id>/partners/<int:partner_id>/', methods=['POST'])
@json
def project_partners(id, partner_id):
    project = Project.query.get_or_404(id)
    partner = Organization.query.get_or_404(partner_id)
    project_partner = ProjectPartner(project=project, organization=partner)
    db.session.add(project_partner)
    db.session.commit()
    return {}, 201


@api.route('/projects/<int:id>/partner/', methods=['GET'])
@json
@paginate('partners')
def get_project_partner(id):
    project = Project.query.get_or_404(id)
    return project.project_partner


@api.route('/projects/<int:id>/agents/', methods=['GET'])
@json
@paginate('project_agents')
def get_projects_agent(id):
    project = Project.query.get_or_404(id)
    return project.project_agent





