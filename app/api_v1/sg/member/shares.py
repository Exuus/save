from ... import api
from ....models import SavingGroupMember, SgMemberContributions, SavingGroup, and_
from ....decorators import json, paginate, no_cache


@api.route('/members/<int:id>/shares/')
@json
def get_member_shares(id):
    pass

