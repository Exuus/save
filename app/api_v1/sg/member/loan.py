from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SavingGroupMember, and_, SavingGroupWallet, \
    MemberLoan, MemberApprovedLoan, MemberLoanRepayment, MemberWriteOff
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
    cycle = SavingGroupCycle.current_cycle(member.saving_group_id)
    if member:
        return MemberLoan.query\
            .join(MemberApprovedLoan, SavingGroupCycle)\
            .filter(MemberLoan.sg_member_id == member.id)\
            .filter(MemberLoan.id == MemberApprovedLoan.loan_id)\
            .filter(MemberLoan.sg_cycle_id == SavingGroupCycle.id)\
            .filter(SavingGroupCycle.id == cycle.id)\
            .filter(MemberApprovedLoan.status == 1)
        # return MemberLoan.query\
        #     .filter(MemberLoan.sg_member_id == member.id)\
        #     .join(SavingGroupCycle)\
        #     .filter(SavingGroupCycle.saving_group_id == member.saving_group_id)\
        #     .join(MemberApprovedLoan)\
        #     .filter(MemberApprovedLoan.status == 1)\
        #     .filter(MemberLoan.id == MemberApprovedLoan.loan_id)
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
        return member.approved_loan.filter_by(status=2)
    return {}, 404


@api.route('/members/<int:id>/loan/', methods=['GET'])
@json
def get_member_loan(id):
    member = SavingGroupMember.query.get_or_404(id)
    try:
        loan = MemberLoan.query\
            .filter_by(sg_member_id=member.id)\
            .order_by(MemberLoan.date_payment.desc())\
            .first()
        status = MemberLoan.loan_status(loan.id, member.saving_group_id)
        loan = MemberLoan.get_loan_balance(loan)
        if not status:
            loan['status'] = 'pending'
            return loan
        return loan
    except AttributeError:
        return {}, 404


@api.route('/member/<int:id>/loan/', methods=['POST'])
@json
def new_loan_request(id):
    member = SavingGroupMember.query.get_or_404(id)
    admins = SavingGroupMember.group_admin(member.saving_group_id)
    loan = MemberLoan.query\
        .filter_by(sg_member_id=member.id)\
        .order_by(MemberLoan.date_payment.desc())\
        .first()
    if loan:
        loan = MemberLoan.get_loan_balance(loan)
        if loan['status'] == 'payed':
            if member:
                if len(admins.all()):
                    if member.verify_pin(request.json['pin']):
                        MemberLoan.post_loan(member, request.json, admins)
                        return {}, 201

        return {}, 404
    else:
        MemberLoan.post_loan(member, request.json, admins)
        return {}, 201


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

                admins = SavingGroupMember.count_group_admin(member.saving_group_id)[0]
                loan_approved = MemberApprovedLoan.get_approved_loan(approved_loan.loan_id)[0]
                wallet = SavingGroupWallet.wallet(member.saving_group_id)
                wallet_balance = wallet.balance()
                loan = MemberLoan.query.get_or_404(approved_loan.loan_id)
                amount_loaned = MemberLoan.get_loan_balance(loan)['amount_loaned']
                approval = 0
                if admins == loan_approved:
                    approval = 1
                    if amount_loaned > wallet_balance:
                        approved_loan.pending_loan()
                        db.session.add(approved_loan)
                        db.session.commit()
                        return {'status': 'not enough found'}, 404
                    loan.not_payed()
                    wallet.debit_wallet(amount_loaned)
                    db.session.add(loan)
                    db.session.add(wallet)
                    db.session.commit()
                return {}, 200, {'Loan-Approval': approval}
        except AttributeError:
            return {}, 404
    return {'status': 'Wrong PIN'}, 404


@api.route('/loan/<int:id>/transactions-id/', methods=['PUT'])
@json
def put_loan_transaction_id(id):
    loan = MemberLoan.query.get_or_404(id)
    loan.update_transaction_id()
    db.session.add(loan)
    db.session.commit()
    return {}, 200


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


@api.route('/loan/<int:id>/repayment/', methods=['POST'])
@json
def new_loan_repayment(id):
    loan = MemberLoan.query.get_or_404(id)
    balance = MemberLoan.get_loan_balance(loan)
    payed = balance['payed_amount']
    total = balance['total_loan_interest_plus_fine']
    remain = balance['remain_amount']
    wallet = SavingGroupWallet.query.get_or_404(balance['wallet_id'])

    if float(request.json['amount']) > float(remain):
        return {}, 404

    if payed < total:
        loan_repayment = MemberLoanRepayment(member_loan=loan)
        loan_repayment.import_data(request.json)
        wallet.credit_wallet(request.json['amount'])
        db.session.add(loan_repayment)
        db.session.add(wallet)
        db.session.commit()
        balance = MemberLoan.get_loan_balance(loan)
        if balance['status'] == 'payed':
            # update payment date to do
            loan.date_repayment()
            db.session.add(loan)
            db.session.commit()
            return balance
    return MemberLoan.get_loan_balance(loan)


@api.route('/loan/<int:id>/write-off/', methods=['PUT'])
@json
def update_write_off(id):
    admin = SavingGroupMember.query.get_or_404(request.json['admin_id'])
    admins = SavingGroupMember.group_admin(admin.saving_group_id)
    if admin.verify_pin(request.json['pin']):
        loan = MemberLoan.query \
            .filter_by(id=id) \
            .order_by(MemberLoan.date_payment.desc()) \
            .first()
        if MemberLoan.get_loan_balance(loan)['status'] == 'not payed':
            MemberWriteOff.post_write_off(admins, loan)

            loan.write_off(request.json['admin_id'])
            db.session.add(loan)
            db.session.commit()
            return {}, 200
    return {}, 404


@api.route('/write-off/<int:id>/', methods=['GET'])
@json
def get_member_write_off(id):
    return MemberWriteOff.query.get_or_404(id)


@api.route('/members/admin/<int:id>/pending/write-off/', methods=['GET'])
@json
@paginate('member_write_off')
def get_pending_write_off(id):
    member = SavingGroupMember.query.filter_by(id=id, admin=1).first()
    return member.member_write_off.filter_by(status=2)


@api.route('/members/admin/<int:member_id>/approve/write-off/<int:id>/', methods=['PUT'])
@json
def approve_write_off(member_id, id):
    member = SavingGroupMember.query.filter_by(id=member_id, admin=1).first()
    if member:
        if member.verify_pin(request.json['pin']):
            approved_write_off = MemberWriteOff.query.get_or_404(id)
            approved_write_off.approve_write_off()
            db.session.add(approved_write_off)
            db.session.commit()

            admins = SavingGroupMember.count_group_admin(member.saving_group_id)
            write_off_approved = MemberWriteOff.get_approved(approved_write_off.loan_id)
            approval = 0
            if admins == write_off_approved:
                approval = 1
                loan = MemberLoan.query.get_or_404(approved_write_off.loan_id)
                loan.write_off(request.json['member_id'])
                db.session.add(loan)
                db.session.commit()
            return {}, 200 , {'Write-Off-Approval': approval}
    return {'status': 'Wrong PIN'}, 404


@api.route('/members/admin/<int:member_id>/decline/write-off/<int:id>/', methods=['PUT'])
@json
def decline_write_off(member_id, id):
    member = SavingGroupMember.query.filter_by(id=member_id, admin=1).first()
    if member:
        if member.verify_pin(request.json['pin']):
            declined_write_off = MemberWriteOff.query.get_or_404(id)
            declined_write_off.decline_write_off()
            approval = 0
            return {}, 200 , {'Write-Off-Approval': approval}
    return {'status': 'Wrong PIN'}, 404


@api.route('/loan/<int:id>/balance/', methods=['GET'])
@json
def get_loan_balance(id):
    loan = MemberLoan.query.get_or_404(id)
    MemberLoan.get_loan_balance(loan)
    return MemberLoan.get_loan_balance(loan)



