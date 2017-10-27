from flask import request
from ... import api
from .... import db
from ....models import SavingGroupMember, and_, User
from ....decorators import json


@api.route('/member/<int:id>', methods=['GET'])
@json
def get_sg_member(id):
    return SavingGroupMember.query.get(id)


@api.route('/member/<int:id>/pin/', methods=['GET'])
@json
def check_member_pin(id):
    member = SavingGroupMember.query.\
        filter(and_(SavingGroupMember.id == id,
                    SavingGroupMember.pin.isnot(None))).first()
    if member:
        return {}, 200
    return {}, 404


@api.route('/member/<int:id>/pin/', methods=['POST'])
@json
def verify_member_pin(id):
    member = SavingGroupMember.query.get_or_404(id)
    if member:
        if member.verify_pin(request.json['pin']):
            return {}, 200, {'Location': member.get_url()}
    return {}, 404


@api.route('/member/<int:id>/pin/', methods=['PUT'])
@json
def add_pin(id):
    member = SavingGroupMember.query.get_or_404(id)
    member.set_pin(request.json['pin'])
    db.session.add(member)
    db.session.commit()
    return {}, 200


@api.route('/members/<int:id>/reset-pin/', methods=['PUT'])
@json
def reset_pin(id):
    agent_id = request.json['agent_id']
    agent_password = request.json['agent_password']
    agent = User.query.get_or_404(agent_id)

    if agent.verify_password(agent_password):
        member = SavingGroupMember.query.get_or_404(id)
        member.reset_pin()

    return {}, 200
