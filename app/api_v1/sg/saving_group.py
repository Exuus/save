from flask import request
from .. import api
from ... import db
from ...models import SavingGroup, SavingGroupMember, SavingGroupWallet, \
    Project, Organization, SavingGroupCycle, SavingGroupFinDetails, \
    SavingGroupFines, SavingGroupShares, and_
from ...decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError
from ...errorhandlers import internal_server_error


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

    """ SG Creations """

    project = Project.query.get_or_404(id)
    saving_group = SavingGroup(project=project)
    saving_group.import_data(request.json['saving_group'])
    try:
        db.session.add(saving_group)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return internal_server_error()

    """ SG  Wallet Creation """

    sg_wallet = SavingGroupWallet(saving_group=saving_group)
    db.session.add(sg_wallet)
    db.session.commit()

    """ SG Cycle creation """

    cycle = SavingGroupCycle(saving_group=saving_group)
    cycle.import_data(request.json['cycle'])
    try:
        db.session.add(cycle)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return internal_server_error()

    """ SG Financial details creation """

    for financial in request.json['financial_details']:
        fin_details = SavingGroupFinDetails(saving_group=saving_group)
        fin_details.import_data(financial)
        db.session.add(fin_details)
        db.session.commit()

    """ SG Fines """
    sg_fines = SavingGroupFines(saving_group=saving_group, sg_cycle=cycle)
    sg_fines.import_data(request.json['fines'])
    db.session.add(sg_fines)
    db.session.commit()

    """ SG Shares """
    sg_shares = SavingGroupShares(saving_group=saving_group, sg_cycle=cycle)
    sg_shares.import_data(request.json['shares'])
    db.session.add(sg_shares)
    db.session.commit()

    return {}, 201, {'Location': saving_group.get_url()}


@api.route('/organizations/<int:id>/sg/', methods=['GET'])
@no_cache
@json
@paginate('saving_group')
def get_organizations_sg(id):
    organization = Organization.query.get_or_404(id)
    return organization.saving_group


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
    try:
        db.session.add(member)
        db.session.commit()
        return {}, 201, {'Location': member.get_url()}
    except IntegrityError:
        return internal_server_error()


@api.route('/sg/<int:id>/fines/', methods=['POST'])
@json
def new_sg_fines(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.query.\
        filter(and_(SavingGroupCycle.active == 1,
                    SavingGroupCycle.saving_group_id == saving_group.id)).first()

    sg_fines = SavingGroupFines(saving_group=saving_group, sg_cycle=cycle)
    sg_fines.import_data(request.json)
    try:
        db.session.add(sg_fines)
        db.session.commit()
        return {}, 200, {'Location': sg_fines.get_url()}
    except IntegrityError:
        return internal_server_error()


@api.route('/fines/<int:id>/', methods=['PUT'])
@json
def edit_fines(id):
    fines = SavingGroupFines.query.get_or_404(id)
    fines.import_data(request.json)
    db.session.add(fines)
    db.session.commit()
    return {}, 200


@api.route('/sg/<int:id>/fines/', methods=['GET'])
@json
def get_sg_current_fines(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.query. \
        filter(and_(SavingGroupCycle.active == 1,
                    SavingGroupCycle.saving_group_id == saving_group.id)).first()

    return SavingGroupFines.query.filter_by(sg_cycle_id=cycle.id).first()


@api.route('/sg/<int:id>/shares/', methods=['POST'])
@json
def new_sg_shares(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.query.\
        filter(and_(SavingGroupCycle.active == 1,
                    SavingGroupCycle.saving_group_id == saving_group.id)).first()

    sg_shares = SavingGroupShares(saving_group=saving_group, sg_cycle=cycle)
    sg_shares.import_data(request.json)
    try:
        db.session.add(sg_shares)
        db.session.commit()
        return {}, 200, {'Location': sg_shares.get_url()}
    except IntegrityError:
        return internal_server_error()


@api.route('/shares/<int:id>/', methods=['PUT'])
@json
def edit_shares(id):
    shares = SavingGroupShares.query.get_or_404(id)
    shares.import_data(request.json)
    db.session.add(shares)
    db.session.commit()
    return {}, 200


@api.route('/sg/<int:id>/shares/', methods=['GET'])
@json
def get_sg_current_shares(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.query.\
        filter(and_(SavingGroupCycle.active == 1,
                    SavingGroupCycle.saving_group_id == saving_group.id)).first()

    return SavingGroupShares.query.filter_by(sg_cycle_id=cycle.id).first()
