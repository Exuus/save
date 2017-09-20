from flask import request
from . import api
from .. import db
from ..models import Project, Organization, User, ProjectAgent
from ..decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError


@api.route('/projects/<int:id>', methods=['GET'])
@json
def get_project(id):
    return Project.query.get_or_404(id)


@api.route('/organizations/<int:id>/projects/', methods=['GET'])
@json
@paginate('projects')
def get_organization_projects(id):
    organization = Organization.query.get_or_404(id)
    return organization.project


@api.route('/users/<int:id>/projects/', methods=['GET'])
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
    return {}, 201, {'Location': project.get_url()}


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