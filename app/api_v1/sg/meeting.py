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

    return meeting


@api.route('/attendees/<int:id>/')
@json
def get_attendee(id):
    attendee = MeetingAttendance.query.get_or_404(id)
    return attendee


@api.route('/meetings/<int:id>/attendees/', methods=['GET'])
@no_cache
@json
@paginate('meeting_attendees')
def get_meeting_attendee(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    return meeting.meeting_attendance


@api.route('/meetings/<int:id>/attendees/', methods=['POST'])
@json
def new_meeting_attendance(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    members = request.json
    for member in members:
        member = SavingGroupMember.query.get_or_404(member['member_id'])
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


@api.route('/meetings/<int:id>/attendees/', methods=['DELETE'])
@json
def remove_attendees(id):
    meeting = SavingGroupMeeting.query.get_or_404(id)
    members = request.json
    for member in members:
        member = SavingGroupMember.query.get_or_404(member['member_id'])
        attendance = MeetingAttendance(sg_meeting=meeting, sg_member=member)
        db.session.delete(attendance)
        db.session.commit()
    return {}, 200
