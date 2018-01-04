from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SavingGroupMember, \
    SavingGroupDropOut, MemberLoan, SavingGroup, and_, DropOutApproved, \
    SavingGroupShareOut, DropOutShareOut
from ....decorators import json, paginate, no_cache


@api.route('/drop-out/<int:id>/', methods=['GET'])
@json
def get_member_drop(id):
    return SavingGroupDropOut.query.get_or_404(id)


@api.route('/drop-out/approved/<int:id>/', methods=['GET'])
@json
def get_drop_out_approved(id):
    return DropOutApproved.query.get_or_404(id)


@api.route('/members/<int:id>/drop-out/', methods=['POST'])
@json
def drop_out(id):
    member = SavingGroupMember.query.get_or_404(id)
    admins = SavingGroupMember.group_admin(member.saving_group_id)
    if member.verify_pin(request.json['pin']):
        cycle = SavingGroupCycle.current_cycle(member.saving_group_id)

        try:
            loan = MemberLoan.query \
                .filter_by(sg_member_id=member.id) \
                .order_by(MemberLoan.date_payment.desc()) \
                .first()
            loan = MemberLoan.get_loan_balance(loan)
            if loan['status'] == 'payed':
                SavingGroupDropOut.post_drop_out(member, cycle, admins)
                return {}, 201
        except AttributeError:
            SavingGroupDropOut.post_drop_out(member, cycle, admins)
            return {}, 201

    return {}, 404


@api.route('/members/admin/<int:id>/drop-out/pending/', methods=['GET'])
@no_cache
@json
@paginate('pending_drop_out')
def get_pending_drop_out(id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == id)).\
        first()

    if member:
        return member.admin_drop_out_approved.filter_by(status=2)
    return {}, 404


@api.route('/members/admin/<int:member_id>/approve/drop-out/<int:id>/', methods=['PUT'])
@json
def approve_drop_out(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()

    if member:

        if member.verify_pin(request.json['pin']):
            approved_drop_out = DropOutApproved.query.get_or_404(id)
            approved_drop_out.approve_drop_out()
            db.session.add(approved_drop_out)
            db.session.commit()

            admins = SavingGroupMember.count_group_admin(member.saving_group_id)[0]
            drop_out_approved = DropOutApproved.get_approved_drop_out(approved_drop_out.drop_out_id)[0]

            sg_drop_out = SavingGroupDropOut.query.get_or_404(approve_drop_out.drop_out_id)
            member = SavingGroupMember.query.get_or_404(drop_out.member_id)
            approval = 0
            if admins == drop_out_approved:
                approval = 1
            return {}, 200, {
                                'Drop-Out-Approval': approval,
                                'Location': member.get_member_share_out(),
                                'drop_out_id': sg_drop_out.id
                             }

            # Remain headers Location for member share out
            # drop out id to the headers

        # except AttributeError:
        #     return {}, 404
    return {'status': 'Wrong PIN'}, 404


@api.route('/member/<int:id>/share-out/', methods=['GET'])
@json
def get_member_share_out_drop_out(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member.activate == 1:
        if SavingGroupShareOut.member_share_out(member) is False:
            return {}, 404
        return SavingGroupShareOut.member_share_out(member)
    return {}, 404


@api.route('/members/admin/<int:member_id>/decline/drop-out/<int:id>/', methods=['PUT'])
@json
def decline_drop_out(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()

    if member:

        if member.verify_pin(request.json['pin']):
            declined_drop_out = DropOutApproved.query.get_or_404(id)
            declined_drop_out.decline_drop_out()
            db.session.add(declined_drop_out)
            db.session.commit()
            approval = 0
            return {}, 200, {'Drop-Out-Approval': approval}

        # except AttributeError:
        #     return {}, 404
    return {'status': 'Wrong PIN'}, 404


@api.route('/sg/<int:id>/drop-out/', methods=['GET'])
@no_cache
@json
@paginate('drop_out')
def get_sg_drop_out(id):
    return SavingGroupDropOut.query\
        .join(SavingGroupMember, SavingGroup)\
        .filter(SavingGroupMember.id == SavingGroupDropOut.member_id)\
        .filter(SavingGroupMember.saving_group_id == SavingGroup.id)\
        .filter(SavingGroup.id == id)


@api.route('/drop-out/share-out/<int:id>/', methods=['GET'])
@json
def get_drop_out_share_out(id):
    return DropOutShareOut.query.get_or_404(id)


@api.route('/member/<int:id>/drop-share-out/', methods=['POST'])
@json
def new_member_drop_share_out(id):
    member = SavingGroupMember.query.get_or_404(id)
    sg_drop_out = SavingGroupDropOut.query.get_or_404(request.json['drop_out_id'])
    drop_share_out = DropOutShareOut(sg_member=member, sg_drop_out=sg_drop_out)
    drop_share_out.import_data(request.json)
    db.session.add(drop_share_out)
    db.session.commit()
    return {}, 201


