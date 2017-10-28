from flask import request
from .. import api
from ...models import SavingGroup, SavingGroupMember, SavingGroupMeeting, \
    MeetingAttendance, SavingGroupCycle, db
from ...decorators import json, paginate, no_cache


@api.route('/meetings/<int:id>/', methods=['GET'])
@json
def get_meeting(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    return meeting


@api.route('/sg/<int:id>/meetings/', methods=['GET'])
@no_cache
@json
@paginate('sg_meetings')
def get_sg_meetings(id):
    saving_group = SavingGroup.query.get_or_404(id)
    return saving_group.sg_meeting


@api.route('/sg/<int:id>/meetings/', methods=['POST'])
@json
def new_sg_meetings(id):
    saving_group = SavingGroup.query.get_or_404(id)
    cycle = SavingGroupCycle.current_cycle(id)
    meeting = SavingGroupMeeting(sg_cycle=cycle,
                                 saving_group=saving_group)
    meeting.import_data(request.json)
    db.session.add(meeting)
    db.session.commit()

    return {}, 200, {'Location': meeting.get_url()}


@api.route('/meetings/<int:id>/members/', methods=['POST'])
@json
def meeting_attendance(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    members = request.json
    for member in members:
        member = SavingGroupMember.query.get_or_404(member['id'])
        attendance = MeetingAttendance(sg_meeting=meeting, sg_member=member)
        db.session.add(attendance)
        db.session.commit()
    return {}, 200


@api.route('/meetings/<int:id>/', methods=['PUT'])
@json
def edit_meetings(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    meeting.import_data(request.json)
    db.session.add(meeting)
    db.session.commit()
    return {}, 200


@api.route('/meetings/<int:id>/members/', methods=['DELETE'])
@json
def remove_attendance(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    members = request.json
    for member in members:
        member = SavingGroupMember.query.get_or_404(member['id'])
        attendance = MeetingAttendance(sg_meeting=meeting, sg_member=member)
        db.session.delete(attendance)
        db.session.commit()
    return {}, 200
