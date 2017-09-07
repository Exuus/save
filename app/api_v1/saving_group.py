from flask import request
from . import api
from .. import db
from ..models import SavingGroup, SavingGroupCycle, SavingGroupDropOut,\
    SavingGroupFinDetails, SavingGroupMember, SavingGroupWallet, \
    SgApprovedLoan, SgApprovedSocialDebit, SgMemberContributions, \
    Project, ProjectAgent, Organization
from ..decorators import json, paginate, no_cache
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


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
    sg = SavingGroup(project=project)
    sg.import_data(request.json)
    db.session.add(sg)
    db.session.commit()

    """ SG  Wallet Creation """

    sg_wallet = SavingGroupWallet(saving_group=sg)
    db.session.add(sg_wallet)
    db.session.commit()

    return {}, 201, {'Location': sg.get_url()}


@api.route('/cycle/<int:id>', methods=['GET'])
@json
def get_cycle(id):
    return SavingGroupCycle.query.get_or_404(id)


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


@api.route('/member/<int:id>', methods=['GET'])
@json
def get_sg_member(id):
    return SavingGroupMember.query.get(id)


@api.route('/member/<int:id>/pin/', methods=['GET'])
@json
def check_member_pin(id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.id == id,
                    SavingGroupMember.pin.isnot(None))).first()
    if member:
        return {}, 200
    return {}, 404


@api.route('/member/<int:id>/pin/', methods=['POST'])
@json
def verify_member_pin(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        if member.verify_pin(request.json['pin']):
            return {}, 200, {'Location': member.get_url()}
    return {}, 404


@api.route('/member/<int:id>/pin/', methods=['PUT'])
@json
def add_pin(id):
    member = SavingGroupMember.query.get_or_404(id)
    member.set_pin(request.json['pin'])
    db.session.add(member)
    db.session.commit()
    return {}, 200


@api.route('/contributions/<int:id>')
@json
def get_contribution(id):
    return SgMemberContributions.query.get_or_404(id)


@api.route('/member/<int:id>/savings/')
@json
@paginate('member_savings')
def get_member_savings(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.contributions.filter_by(type=1).join(SavingGroupCycle)\
        .filter(and_(SavingGroupCycle.id == SgMemberContributions.sg_cycle_id),
                SavingGroupCycle.active == 1)


@api.route('/member/<int:id>/social-fund/')
@json
@paginate('member_social_fund')
def get_member_social_fund(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.contributions.filter_by(type=2).join(SavingGroupCycle)\
        .filter(and_(SavingGroupCycle.id == SgMemberContributions.sg_cycle_id),
                SavingGroupCycle.active == 1)


@api.route('/member/<int:id>/contributions/', methods=['POST'])
@json
def new_member_savings(id):
    data = request.json
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        if member.verify_pin(data['pin']):
            wallet = SavingGroupWallet.query.\
                filter(SavingGroupWallet.saving_group_id == member.saving_group_id).first()
            cycle = SavingGroupCycle.query.\
                filter(and_(SavingGroupCycle.active == 1,
                            SavingGroupCycle.saving_group_id == member.saving_group_id)).\
                first()

            contributions = SgMemberContributions(sg_cycle=cycle,
                                                  sg_wallet=wallet,
                                                  sg_member=member)
            contributions.import_data(data)
            wallet.credit_wallet(data['amount'])
            db.session.add(contributions)
            db.session.add(wallet)
            db.session.commit()
            return {}, 201, {'Location': contributions.get_url()}

    return {}, 404


@api.route('/member/<int:id>/loan/', methods=['GET'])
@json
def new_loan_request(id):
    pass


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