from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, MemberFine, \
    SavingGroupMember, and_, SavingGroupWallet, SavingGroupFines, MemberFineRepayment
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
    fines = MemberFine.fixed_fine(member.id, cycle.id)
    data = list()
    for fine in fines:
        json = dict()
        json['fine'] = fine[0]
        json['name'] = fine[1]
        json['acronym'] = fine[2]
        json['id'] = fine[3]
        json['payed'] = 0 if MemberFineRepayment.fine_balance(json['id']) is None \
            else MemberFineRepayment.fine_balance(json['id'])
        json['date'] = fine[4]
        json['fine_balance'] = int(json['fine']) - int(json['payed'])
        json['status'] = fine[5]
        data.append(json)

    return data


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


@api.route('/fine-repayment/<int:id>/', methods=['POST'])
@json
def new_fine_repayment(id):
    member = SavingGroupMember.query.get_or_404(request.json['member_id'])
    if member.verify_pin(request.json['pin']):
        member_fine = MemberFine.query.get_or_404(id)
        sg_fines = SavingGroupFines.query.get_or_404(member_fine.sg_fine_id)
        payed = 0 if MemberFineRepayment.fine_balance(member_fine.id) is None \
            else MemberFineRepayment.fine_balance(member_fine.id)
        wallet = SavingGroupWallet.query.get_or_404(member_fine.wallet_id)

        if payed < sg_fines.fine:
            member_fine_repay = MemberFineRepayment(member_fine=member_fine)
            member_fine_repay.import_data(request.json)
            wallet.credit_wallet(request.json['amount'])
            db.session.add(wallet)
            db.session.add(member_fine_repay)
            db.session.commit()

            amount_payed = 0 if MemberFineRepayment.fine_balance(member_fine.id) is None \
                else MemberFineRepayment.fine_balance(member_fine.id)

            if amount_payed == sg_fines:
                member_fine.repay_fine()
                db.session.add(member_fine)
                db.session.commit()

            return {}, 201
    return {}, 404






