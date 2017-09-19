from .. import api
from ...models import SavingGroupWallet, SavingGroup, MemberLoan, SavingGroupCycle, \
    MemberApprovedLoan
from ...decorators import json, paginate, no_cache


@api.route('/wallet/<int:id>', methods=['GET'])
@json
def get_wallet(id):
    wallet = SavingGroupWallet.query.get_or_404(id)
    return wallet


@api.route('/sg/<int:id>/wallet/', methods=['GET'])
@no_cache
@json
@paginate('wallet')
def get_sg_wallet(id):
    saving_group = SavingGroup.query.get_or_404(id)
    import pdb; pdb.set_trace()
    return saving_group.sg_wallet


@api.route('/wallet/<int:id>/loan/')
@no_cache
@json
@paginate('loan')
def get_wallet_loan(id):
    wallet = SavingGroupWallet.query.get_or_404(id)
    if wallet:
        return MemberLoan.query \
            .filter(MemberLoan.sg_wallet_id == wallet.id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.saving_group_id == wallet.saving_group_id) \
            .join(MemberApprovedLoan) \
            .filter(MemberApprovedLoan.status == 1)
    return {}, 404,


