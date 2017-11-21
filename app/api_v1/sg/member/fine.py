from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, MemberFine, \
    SavingGroupMember, and_, SavingGroupWallet, SavingGroupFines
from ....decorators import json, paginate, no_cache


@api.route('/fines/<int:id>/', methods=['GET'])
@json
def get_fine(id):
    return MemberFine.query.get_or_404(id)


@api.route('/members/<int:id>/fines/', methods=['GET'])
@json
def get_member_fine(id):
    member = SavingGroupMember.query.get_or_404(id)
    cycle = SavingGroupCycle.current_cycle(member.saving_group_id)
    return MemberFine.fixed_fine(member.id, cycle.id)


@api.route('/members/<int:id>/fines/<int:fine_id>/', methods=['POST'])
@json
def new_member_fine(id, fine_id):

    member = SavingGroupMember.query.get_or_404(id)

    admin = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1,
                    SavingGroupMember.id == request.json['initiate_by'])).first()

    sg_fines = SavingGroupFines.query.get_or_404(fine_id)

    if admin.verify_pin(request.json['pin']):
        wallet = SavingGroupWallet.query. \
            filter(SavingGroupWallet.saving_group_id == member.saving_group_id).first()

        member_fine = MemberFine(sg_fines=sg_fines,
                                 sg_member=member,
                                 sg_wallet=wallet)

        member_fine.import_data(request.json)
        db.session.add(member_fine)
        db.session.commit()
        return {}, 201, {'Location': member_fine.get_url()}
    return {}, 404


