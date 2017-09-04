from flask import request
from . import api
from .. import db
from ..models import SavingGroup, SavingGroupCycle, SavingGroupDropOut,\
    SavingGroupFinDetails, SavingGroupMember, SavingGroupWallet, \
    SgApprovedLoan, SgApprovedSocialDebit, SgMemberTransaction, \
    Project, ProjectAgent, Organization
from ..decorators import json, paginate, no_cache


@api.route('/sg/<int:id>/', methods=['GET'])
@json
def get_sg(id):
    return SavingGroup.query.get_or_404(id)


@api.route('/projects/<int:id>/sg/', methods=['GET'])
@no_cache
@json
@paginate('saving_group')
def get_project_sgs(id):
    project = Project.query.get_or_404(id)
    return project.saving_group


@api.route('/project/<int:id>/sg/', methods=['POST'])
@json
def new_saving_group(id):
    project = Project.query.get_or_404(id)
    sg = SavingGroup(project=project)
    sg.import_data(request.json)
    db.session.add(sg)
    db.session.commit()
    return {}, 201, {'Location': sg.get_url()}


@api.route('/member/<int:id>', methods=['GET'])
@json
def get_sg_member(id):
    return SavingGroupMember.query.get(id)


@api.route('/sg/<int:id>/members/', methods=['GET'])
@no_cache
@json
@paginate('members')
def get_sg_members(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return saving_group.sg_member


@api.route('/sg/<int:id>/members/', methods=['POST'])
@json
def new_sg_member(id):
    saving_group = SavingGroup.query.get_or_404(id)
    member = SavingGroupMember(saving_group=saving_group)
    member.import_data(request.json)
    db.session.add(member)
    db.session.commit()
    return {}, 201, {'Location': member.get_url()}