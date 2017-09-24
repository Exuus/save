from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, MemberFine, \
    SavingGroupMember, and_, SavingGroupWallet
from ....decorators import json, paginate, no_cache


@api.route('/fine/<int:id>', methods='GET')
@json
def get_fine(id):
    return MemberFine.query.get_or_404(id)


@api.route('/members/<int:id>/fine/', methods=['GET'])
@no_cache
@json
@paginate('fine')
def get_member_fine(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.member_fine


@api.route('/members/admin/<int:id>/fine/', methods=['POST'])
@json
def new_member(id):
    member = SavingGroupMember.query.get_or_404(id)
    admin = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1,
                    SavingGroupMember.id == request.json['initiate_by']))
    if admin.verify_pin(request.json['pin']):
        cycle = SavingGroupCycle.query.get_or_404(request.json['cycle_id'])
        wallet = SavingGroupWallet.query.get_or_404(request.json['wallet_id'])
        member_fine = MemberFine(sg_cycle=cycle,
                                 sg_member=member,
                                 sg_wallet=wallet)

        member_fine.import_data(request.json)
        db.session.add(member_fine)
        db.session.commit()
        return {}, 201, {'Location': member_fine.get_url()}
    return {}, 404


