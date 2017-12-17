from flask import request
from .. import api
from ... import db
from ...models import SavingGroupCycle, SavingGroup, MemberSocialFund, \
    MemberApprovedSocial, MemberApprovedLoan, MemberLoan
from ...decorators import json, paginate, no_cache
from sqlalchemy.exc import IntegrityError


@api.route('/cycles/<int:id>/', methods=['GET'])
@json
def get_cycle(id):
    return SavingGroupCycle.query.get_or_404(id)


@api.route('/sg/<int:id>/cycles/', methods=['GET'])
@no_cache
@json
@paginate('cycles')
def get_sg_cycle(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return saving_group.sg_cycle


@api.route('/sg/<int:id>/cycles/', methods=['POST'])
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


@api.route('/cycles/<int:id>/loan/', methods=['GET'])
@no_cache
@json
@paginate('loan')
def get_cycle_loan(id):
    cycle = SavingGroupCycle.query.get_or_404(id)
    if cycle:
        return MemberLoan.query \
            .filter(MemberLoan.sg_cycle_id == cycle.id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.saving_group_id == cycle.saving_group_id) \
            .join(MemberApprovedLoan) \
            .filter(MemberApprovedLoan.status == 1)
    return {}, 404


@api.route('/cycles/<int:id>/social-fund/debit/', methods=['GET'])
@no_cache
@json
@paginate('social_fund_debit')
def get_cycle_social_fund_debit(id):
    cycle = SavingGroupCycle.query.get_or_404(id)
    if cycle:
        return MemberSocialFund.query \
            .filter(MemberSocialFund.sg_cycle_id == cycle.id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.saving_group_id == cycle.saving_group_id) \
            .join(MemberApprovedSocial) \
            .filter(MemberApprovedSocial.status == 1)
    return {}, 404


@api.route('/cycles/<int:id>/social-fund/credit/', methods=['GET'])
@no_cache
@json
@paginate('social_fund_credit')
def get_cycle_social_fund_credit(id):
    cycle = SavingGroupCycle.query.get_or_404(id)
    if cycle:
        return cycle.contributions.filter_by(type=2)
    return {}, 404


@api.route('/cycles/<int:id>/savings/', methods=['GET'])
@no_cache
@json
@paginate('savings')
def get_cycle_savings(id):
    cycle = SavingGroupCycle.query.get_or_404(id)
    if cycle:
        return cycle.contributions.filter_by(type=1)
    return {}, 404


@api.route('/cycles/<int:id>/members/', methods=['GET'])
@no_cache
@json
@paginate('members')
def get_cycles_members(id):
    cycle = SavingGroupCycle.query.get_or_404(id)
    return cycle.sg_member
