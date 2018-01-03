from flask import request
from .. import api
from ... import db
from ...models import SavingGroupShareOut, SavingGroupCycle, \
    SavingGroup, SavingGroupWallet, MemberShareOut, \
    SavingGroupMember, and_, ApprovedShareOut
from ...decorators import json, paginate, no_cache


@api.route('/share-out/<int:id>/', methods=['GET'])
@json
def get_share_out(id):
    return SavingGroupShareOut.query.get_or_404(id)


@api.route('/sg/<int:id>/share-out/', methods=['POST'])
@json
def new_share_out(id):
    member = SavingGroupMember.query.get_or_404(request.json['admin_id'])
    if member.verify_pin(request.json['pin']):
        admins = SavingGroupMember.group_admin(id)
        sg = SavingGroup.query.get_or_404(id)
        cycle = SavingGroupCycle.current_cycle(sg.id)

        wallet = SavingGroupWallet.wallet(sg.id)
        share_out = wallet.share_out(request.json['shared_amount'])
        SavingGroupShareOut.post_share_out(cycle, share_out, admins, request.json['admin_id'])

        return {}, 200
    return {}, 404


@api.route('/share-out/approved/<int:id>/', methods=['GET'])
@json
def get_approved_share_out(id):
    return ApprovedShareOut.query.get_or_404(id)


@api.route('/members/admin/<int:id>/pending/share-out/', methods=['GET'])
@json
@paginate('pending_share_out')
def get_pending_share_out(id):
    member = SavingGroupMember.query.filter_by(id=id, admin=1).first()
    return member.approved_share_out.filter_by(status=2)


@api.route('/members/admin/<int:member_id>/approve/share-out/<int:id>/', methods=['PUT'])
@json
def approve_share_out(member_id, id):
    member = SavingGroupMember.query. \
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)). \
        first()
    if member:
        if member.verify_pin(request.json['pin']):
            approved_share_out = ApprovedShareOut.query.get_or_404(id)
            approved_share_out.approve_share_out()
            db.session.add(approved_share_out)
            db.session.commit()

            share_out = SavingGroupShareOut.query.get_or_404(approved_share_out.share_out_id)

            share_out_approved = ApprovedShareOut.get_approved_share_out(share_out.id)
            admins = SavingGroupMember.count_group_admin(member.saving_group_id)

            approval = 0
            if share_out_approved == admins:
                approval = 1
            return {}, 200, {
                                'Share-Out-Approval': approval,
                                'Location': share_out.get_members_share_out(),
                                'id': id
                        }

    return {'status': 'Wrong PIN'}, 404


@api.route('/share-out/<int:id>/members/', methods=['GET'])
@json
def get_share_out_members(id):
    share_out = SavingGroupShareOut.query.get_or_404(id)
    cycle = SavingGroupCycle.query.get_or_404(share_out.cycle_id)
    return SavingGroupShareOut.share_out(cycle.saving_group_id, share_out.shared_amount)


@api.route('/share-out/<int:id>/done/', methods=['put'])
@json
def update_share_out_done(id):
    share_out = SavingGroupShareOut.query.get_or_404(id)
    share_out.share_out_done()
    db.session.add(share_out)
    db.session.commit()
    return {}, 200


@api.route('/members/<int:id>/share-out/', methods=['POST'])
@json
def new_members_share_out(id):
    member = SavingGroupMember.query.get_or_404(id)
    share_out = MemberShareOut.query.get_or_404(request.json['share_out_id'])
    member_share_out = MemberShareOut(sg_member=member, sg_share_out=share_out)
    member_share_out.import_data(request.json)
    db.session.add(member_share_out)
    db.session.commit()
    return {}, 201


@api.route('/members/admin/<int:member_id>/decline/share-out/<int:id>/', methods=['PUT'])
@json
def decline_share_out(member_id, id):
    member = SavingGroupMember.query. \
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)). \
        first()
    if member:
        if member.verify_pin(request.json['pin']):
            declined_share_out = ApprovedShareOut.query.get_or_404(id)
            declined_share_out.decline_share_out()
            db.session.add(declined_share_out)
            db.session.commit()

            approval = 0
            return {}, 200, {'Share-Out-Approval': approval}

    return {'status': 'Wrong PIN'}, 404


@api.route('/members/share-out/<int:id>/', methods=['GET'])
@json
def get_member_share_out(id):
    return MemberShareOut.query.get_or_404(id)








