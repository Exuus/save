from ... import api
from ....models import SavingGroupMember, SgMemberContributions, SavingGroup, \
    SavingGroupCycle, SavingGroupShares, and_
from ....decorators import json, paginate, no_cache


@api.route('/members/<int:id>/shares/')
@json
def get_member_shares(id):
    member = SavingGroupMember.query.get_or_404(id)
    cycle = SavingGroupCycle.current_cycle(member.saving_group.id)
    sg_shares = SavingGroupShares.query.\
        filter(SavingGroupShares.sg_cycle_id == cycle.id).first()
    member_savings = SgMemberContributions.sum_savings(member.id)

    return {
        'shares': '{}'.format(sg_shares.calculate_shares(member_savings[0]))
    }


@api.route('/sg/<int:id>/members/shares/')
@no_cache
@json
@paginate('members_shares')
def get_sg_members_shares(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return saving_group.sg_member


