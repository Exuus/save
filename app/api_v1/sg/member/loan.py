from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SavingGroupMember, and_, SavingGroupWallet, \
    MemberLoan, MemberApprovedLoan
from ....decorators import json, paginate, no_cache


@api.route('/loan/<int:id>')
@json
def get_loan(id):
    return MemberLoan.query.get_or_404(id)


@api.route('/member/<int:id>/loan/pending/', methods=['GET'])
@no_cache
@json
@paginate('member_loan')
def get_member_pending_loan(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        return MemberLoan.query\
            .filter(MemberLoan.sg_member_id == member.id)\
            .join(SavingGroupCycle)\
            .filter(SavingGroupCycle.saving_group_id == member.saving_group_id)\
            .join(MemberApprovedLoan)\
            .filter(MemberApprovedLoan.status == 2)
    return {}, 404,


@api.route('/member/<int:id>/loan/approve/', methods=['GET'])
@no_cache
@json
@paginate('member_loan')
def get_member_approve_loan(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        return MemberLoan.query\
            .filter(MemberLoan.sg_member_id == member.id)\
            .join(SavingGroupCycle)\
            .filter(SavingGroupCycle.saving_group_id == member.saving_group_id)\
            .join(MemberApprovedLoan)\
            .filter(MemberApprovedLoan.status == 1)
    return {}, 404,


@api.route('/approved/loan/<int:id>', methods=['GET'])
@json
def get_approved_loan(id):
    return MemberApprovedLoan.query.get_or_404(id)


@api.route('/member/admin/<int:id>/loan/pending/', methods=['GET'])
@no_cache
@json
@paginate('pending_loan')
def get_admin_pending_loan(id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == id)).\
        first()
    if member:
        return member.approved_loan
    return {}, 404


@api.route('/member/<int:id>/loan/', methods=['POST'])
@json
def new_loan_request(id):
    member = SavingGroupMember.query.get_or_404(id)
    admins = SavingGroupMember.group_admin(member.saving_group_id)

    if member:
        if len(admins.all()):
            if member.verify_pin(request.json['pin']):
                wallet = SavingGroupWallet.query. \
                    filter(SavingGroupWallet.saving_group_id == member.saving_group_id).first()
                cycle = SavingGroupCycle.query. \
                    filter(and_(SavingGroupCycle.active == 1,
                                SavingGroupCycle.saving_group_id == member.saving_group_id)). \
                    first()
                loan = MemberLoan(
                    sg_cycle=cycle,
                    sg_wallet=wallet,
                    sg_member=member
                )

                loan.import_data(request.json)
                db.session.add(loan)
                db.session.commit()

                """ add member approve Request """

                for admin in admins:
                    data = dict()
                    data['status'] = 2
                    data['sg_member_id'] = admin.export_data()['id']
                    approved_loan = MemberApprovedLoan(member_loan=loan)
                    approved_loan.import_data(data)
                    db.session.add(approved_loan)
                    db.session.commit()
                return {}, 201, {'Location': loan.get_url()}

    return {}, 404


@api.route('/member/admin/<int:member_id>/approve/loan/<int:id>/', methods=['PUT'])
@json
def approve_loan(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()
    if member:
        try:
            if member.verify_pin(request.json['pin']):
                approved_loan = MemberApprovedLoan.query.get_or_404(id)
                approved_loan.approve_loan()
                db.session.add(approved_loan)
                db.session.commit()
                return {}, 200
        except AttributeError:
            return {}, 404
    return {}, 404


@api.route('/member/admin/<int:member_id>/decline/loan/<int:id>/', methods=['PUT'])
@json
def decline_loan(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()
    if member:
        try:
            if member.verify_pin(request.json['pin']):
                approved_loan = MemberApprovedLoan.query.get_or_404(id)
                approved_loan.decline_loan()
                db.session.add(approved_loan)
                db.session.commit()
                return {}, 200
        except AttributeError:
            return {}, 404
    return {}, 404