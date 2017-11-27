from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SavingGroupMember, \
    SavingGroupDropOut, MemberLoan
from ....decorators import json, paginate, no_cache


@api.route('/members/<int:id>/drop-out/', methods=['POST'])
@json
def drop_out(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member.verify_pin(request.json['pin']):
        cycle = SavingGroupCycle.current_cycle(member.saving_group_id)
        loan = MemberLoan.query \
            .filter_by(sg_member_id=member.id) \
            .order_by(MemberLoan.date_payment.desc()) \
            .first()
        loan = MemberLoan.get_loan_balance(loan)
        if loan['status'] == 'payed':
            drop = SavingGroupDropOut(sg_member=member,
                                      sg_cycle=cycle)
            member.drop_out()
            db.session.add(drop)
            db.session.add(member)
            db.session.commit()
            return {}, 201
    return {}, 404



