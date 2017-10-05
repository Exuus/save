from flask import request
from ... import api
from .... import db
from ....models import SavingGroupMember, SavingGroupWallet, \
    MemberLoan, MemberFine, SgMemberContributions, SavingGroupCycle, and_
from ....decorators import json, paginate, no_cache


@api.route('/members/<int:id>/mini-statement/contributions/')
@no_cache
@json
@paginate('mini_statement_contributions')
def get_members_mini_statement(id):
    member = SavingGroupMember.query.get_or_404(id)
    wallet = SavingGroupWallet.wallet(member.saving_group_id)
    cycle = SavingGroupCycle.current_cycle(member.saving_group_id)
    return member.member_contribution.\
        join(SavingGroupCycle, SavingGroupWallet).\
        filter(and_(SgMemberContributions.sg_cycle_id == cycle.id,
                    SgMemberContributions.sg_wallet_id == wallet.id))
