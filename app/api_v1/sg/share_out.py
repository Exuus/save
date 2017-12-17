from flask import request
from .. import api
from ... import db
from ...models import SavingGroupShareOut, SavingGroupCycle, \
    SavingGroup, SavingGroupWallet, SgMemberContributions, SavingGroupShares
from ...decorators import json, paginate, no_cache


@api.route('/share-out/<int:id>/', methods=['GET'])
@json
def get_share_out(id):
    return SavingGroupShareOut.query.get_or_404(id)


@api.route('/sg/<int:id>/share-out/', methods=['POST'])
@json
def new_share_out(id):
    sg = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.current_cycle(sg.id)
    wallet = SavingGroupWallet.wallet(sg.id)
    wallet_balance = wallet.balance()
    share_out = wallet.share_out(request.json['shared_amount'])
    savings = SgMemberContributions.member_savings(sg.id)
    total_savings = SgMemberContributions.total_savings(sg.id)

    # Update SG Share out
    sg_share_out = SavingGroupShareOut(sg_cycle=cycle)
    sg_share_out.import_data(share_out)
    wallet.debit_wallet(request.json['shared_amount'])
    db.session.add(sg_share_out)
    db.session.add(wallet)
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


