from flask import request
from ... import api
from .... import db
from ....models import SavingGroupCycle, SavingGroupMember, and_, SavingGroupWallet, \
    MemberSocialFund, MemberApprovedSocial
from ....decorators import json, paginate, no_cache


@api.route('/social-fund/<int:id>', methods=['GET'])
@json
def get_social_fund(id):
    return MemberSocialFund.query.get_or_404(id)


@api.route('/approve/social-fund/<int:id>')
@json
def get_approve_social_fund(id):
    return MemberApprovedSocial.query.get_or_404(id)


@api.route('/members/<int:id>/social-fund/pending/', methods=['GET'])
@no_cache
@json
@paginate('member_social_fund')
def get_member_pending_social_fund(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        return MemberSocialFund.query\
            .filter(MemberSocialFund.sg_member_id == member.id)\
            .join(SavingGroupCycle)\
            .filter(SavingGroupCycle.saving_group_id == member.saving_group_id)\
            .join(MemberApprovedSocial)\
            .filter(MemberApprovedSocial.status == 2)
    return {}, 404,


@api.route('/members/<int:id>/social-fund/approve/', methods=['GET'])
@no_cache
@json
@paginate('member_social_fund')
def get_member_approve_social_fund(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        return MemberSocialFund.query\
            .filter(MemberSocialFund.sg_member_id == member.id)\
            .join(SavingGroupCycle)\
            .filter(SavingGroupCycle.saving_group_id == member.saving_group_id)\
            .join(MemberApprovedSocial)\
            .filter(MemberApprovedSocial.status == 1)
    return {}, 404,


@api.route('/members/admin/<int:id>/social-fund/pending/', methods=['GET'])
@no_cache
@json
@paginate('pending_social_fund')
def get_admin_pending_social(id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == id)).\
        first()
    if member:
        return member.approve_social
    return {}, 404


@api.route('/members/<int:id>/social-fund/', methods=['POST'])
@json
def member_social_fund_request(id):
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
                social_fund = MemberSocialFund(
                    sg_cycle=cycle,
                    sg_wallet=wallet,
                    sg_member=member
                )

                social_fund.import_data(request.json)
                db.session.add(social_fund)
                db.session.commit()

                """ add member approve Request """

                for admin in admins:
                    data = dict()
                    data['status'] = 2
                    data['sg_member_id'] = admin.export_data()['id']
                    approve_social = MemberApprovedSocial(member_social_fund=social_fund)
                    approve_social.import_data(data)
                    db.session.add(approve_social)
                    db.session.commit()
                return {}, 201, {'Location': social_fund.get_url()}

    return {}, 404


@api.route('/members/admin/<int:member_id>/approve/social-fund/<int:id>/', methods=['PUT'])
@json
def approve_social(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()

    if member:
        try:
            if member.verify_pin(request.json['pin']):

                approved_social = MemberApprovedSocial.query.get_or_404(id)
                approved_social.approve_social()
                db.session.add(approved_social)
                db.session.commit()

                admins = SavingGroupMember.count_group_admin(member.saving_group_id)[0]
                approve_social_fund = MemberApprovedSocial.get_approved_social_fund(approved_social.social_debit_id)[0]
                approval = 0
                if admins == approve_social_fund:
                    approval = 1

                return {}, 200, {'Social-Fund-Approval': approval}
        except AttributeError:
            return {}, 200
    return {}, 404


@api.route('/members/admin/<int:member_id>/decline/social-fund/<int:id>/', methods=['PUT'])
@json
def decline_social(member_id, id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.admin == 1, SavingGroupMember.id == member_id)).\
        first()
    if member:
        try:
            if member.verify_pin(request.json['pin']):
                approved_social = MemberApprovedSocial.query.get_or_404(id)
                approved_social.decline_social()
                db.session.add(approved_social)
                db.session.commit()
                return {}, 200
        except AttributeError:
            return {}, 404
    return {}, 404


@api.route('/members/<int:id>/admin/<int:as_id>/', methods=['GET'])
@json
def get_admin_member(id, as_id):
    member = SavingGroupMember.query.get_or_404(id)
    admins = SavingGroupMember.count_group_admin(member.saving_group_id)

    return {'admin': admins[0]}



