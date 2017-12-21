from flask import request
from .. import api
from ... import db
from ...models import SavingGroupShareOut, SavingGroupCycle, \
    SavingGroup, SavingGroupWallet, SgMemberContributions, SavingGroupShares, \
    SavingGroupMember
from ...decorators import json, paginate, no_cache
from datetime import date


@api.route('/share-out/<int:id>/', methods=['GET'])
@json
def get_share_out(id):
    return SavingGroupShareOut.query.get_or_404(id)


@api.route('/sg/<int:id>/share-out/', methods=['POST'])
@json
def new_share_out(id):
    member = SavingGroupMember.query.get_or_404(request.json['id'])
    if member.verify_pin(request.json['pin']):
        sg = SavingGroup.query.get_or_404(id)
        cycle = SavingGroupCycle.current_cycle(sg.id)
        wallet = SavingGroupWallet.wallet(sg.id)
        wallet_balance = wallet.balance()
        share_out = wallet.share_out(request.json['shared_amount'])
        savings = SgMemberContributions.member_savings(sg.id)
        total_savings = SgMemberContributions.total_savings(sg.id)

        # Update SG Share out and Wallet
        sg_share_out = SavingGroupShareOut(sg_cycle=cycle)
        sg_share_out.import_data(share_out)
        wallet.debit_wallet(request.json['shared_amount'])
        db.session.add(sg_share_out)
        db.session.add(wallet)
        db.session.commit()

        # Update Cycle
        cycle.deactivate()
        db.session.add(cycle)
        db.session.commit()
        cycle = SavingGroupCycle(saving_group=sg)
        json = dict()
        today = date.today()
        json['start'] = today.strftime('%Y-%m-%d')
        json['end'] = date(today.year + 1, today.month, today.day).strftime('%Y-%m-%d')
        cycle.import_data(json)
        db.session.add(cycle)
        db.session.commit()

        data = list()
        shares = 0
        for saving in savings:
            json = dict()
            json['saving'] = saving[0]
            json['member_id'] = saving[1]
            json['share'] = SavingGroupShares.calculate_shares(saving[0], sg.id)
            json['percentage_share'] = (json['saving']/total_savings) * 100
            json['share_out_amount'] = (json['percentage_share'] * float(share_out['shared_amount']))/100
            shares += json['share']
            data.append(json)
        return data

    return {}, 404


