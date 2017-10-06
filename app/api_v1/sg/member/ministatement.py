from ... import api
from ....models import SavingGroupMember, MemberMiniStatement, SavingGroup, and_
from ....decorators import json, paginate, no_cache


@api.route('/mini-statement/<int:id>/')
@json
def get_mini_statement(id):
    return MemberMiniStatement.query.get_or_404(id)


@api.route('/members/<int:id>/mini-statement/')
@no_cache
@json
@paginate('member_mini_statement')
def get_members_mini_statement(id):
    member = SavingGroupMember.query.get_or_404(id)
    return member.member_mini_statement


@api.route('/sg/<int:id>/mini-statement/')
@no_cache
@json
@paginate('sg_mini_statement')
def get_sg_mini_statement(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return MemberMiniStatement.query.\
        join(SavingGroupMember, SavingGroup).\
        filter(and_(SavingGroupMember.id == MemberMiniStatement.member_id,
                    SavingGroupMember.saving_group_id == SavingGroup.id,
                    SavingGroup.id == saving_group.id))

