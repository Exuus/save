from flask import request
from .. import api
from ... import db
from ...models import SavingGroupShareOut, SavingGroupCycle, \
    SavingGroup, SavingGroupWallet
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
    return wallet.share_out(request.json['shared_amount'])
