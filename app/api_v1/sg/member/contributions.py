from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SgMemberContributions, \
    SavingGroupMember, and_, SavingGroupWallet
from ....decorators import json, paginate, no_cache


@api.route('/contributions/<int:id>')
@json
def get_contribution(id):
    return SgMemberContributions.query.get_or_404(id)


@api.route('/member/<int:id>/savings/')
@no_cache
@json
@paginate('member_savings')
def get_member_savings(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.contributions.filter_by(type=1).join(SavingGroupCycle)\
        .filter(and_(SavingGroupCycle.id == SgMemberContributions.sg_cycle_id),
                SavingGroupCycle.active == 1)


@api.route('/member/<int:id>/social-fund/')
@no_cache
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