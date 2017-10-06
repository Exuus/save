from ... import api
from ....models import SavingGroupMember, MemberMiniStatement
from ....decorators import json, paginate, no_cache


@api.route('/mini-statement/<int:id>/')
@json
def get_mini_statement(id):
    return MemberMiniStatement.query.get_or_404(id)


@api.route('/members/<int:id>/mini-statement/')
@no_cache
@json
@paginate('mini_statement')
def get_members_mini_statement(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.member_mini_statement

