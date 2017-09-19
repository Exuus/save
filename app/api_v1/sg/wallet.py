from .. import api
from ...models import SavingGroupWallet, SavingGroup, MemberLoan, SavingGroupCycle, \
    MemberApprovedLoan, MemberApprovedSocial, MemberSocialFund, db
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
    return saving_group.sg_wallet


@api.route('/sg/<int:id>/wallet/', methods=['POST'])
@json
def new_sg_wallet(id):
    saving_group = SavingGroup.query.get_or_404(id)
    sg_wallet = SavingGroupWallet(saving_group=saving_group)
    db.session.add(sg_wallet)
    db.session.commit()
    return {}, 201, {'Location': sg_wallet.get_url()}


@api.route('/wallet/<int:id>/loan/', methods=['GET'])
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
    return {}, 404


@api.route('/wallet/<int:id>/social-fund/debit/', methods=['GET'])
@no_cache
@json
@paginate('social_fund_debit')
def get_wallet_social_fund_debit(id):
    wallet = SavingGroupWallet.query.get_or_404(id)
    if wallet:
        return MemberSocialFund.query \
            .filter(MemberSocialFund.sg_wallet_id == wallet.id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.saving_group_id == wallet.saving_group_id) \
            .join(MemberApprovedSocial) \
            .filter(MemberApprovedSocial.status == 1)
    return {}, 404


@api.route('/wallet/<int:id>/social-fund/credit/', methods=['GET'])
@no_cache
@json
@paginate('social_fund_credit')
def get_wallet_social_fund_credit(id):
    wallet = SavingGroupWallet.query.get_or_404(id)
    if wallet:
        return wallet.member_transaction.filter_by(type=2)
    return {}, 404


@api.route('/wallet/<int:id>/savings/', methods=['GET'])
@no_cache
@json
@paginate('savings')
def get_wallet_savings(id):
    wallet = SavingGroupWallet.query.get_or_404(id)
    if wallet:
        return wallet.member_transaction.filter_by(type=1)
    return {}, 404


