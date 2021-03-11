from app.decorator import schedule_information_required
from app.decorator import cancel_applicant_required
from app.decorator import apply_message_required
from app.decorator import handshake_jwt_required
from app.decorator import chat_message_required
from app.decorator import room_token_required
from app.decorator import result_required
from app.decorator import answer_required
from app.decorator import room_writed
from app.decorator import send_alarm
from app.decorator import room_read
from app.models import ClubMember
from app.models import RoomStatus
from app.models import UserType
from app.models import Club
from app.models import User 
from app.models import Club
from app.models import Major
from app.models import Chat
from app.models import Room
from app.models import isoformat
from app.models import kstnow
from app import error
from app import db
from flask_socketio import leave_room
from flask_socketio import join_room
from flask_socketio import emit
from flask import request


# 동아리 지원
@room_token_required
@apply_message_required
@room_writed
@send_alarm
def helper_apply(json):
    '''
    동아리 면접에 지원하는 채팅 봇
    '''
    room = json.get('room')
    date = kstnow()
    major = Major.query.filter_by(club_id=json.get('club_id'), major_name=json.get('major')).first()
    emit('recv_chat', {'title': json.get('title'), 'msg': json.get('msg'), 'user_type': UserType.H1.name, 'date': isoformat(date)}, room=json.get('room_id'))
    db.session.add(Chat(room_id=json.get('room_id'), title=json.get('title'), msg=json.get('msg'), user_type=UserType.H1.name))
    room.status=RoomStatus.A.name
    room.update_room_message(json.get('msg'), date)
    db.session.commit()


# 면접 스케쥴 
@room_token_required
@schedule_information_required
@room_writed
@send_alarm
def helper_schedule(json):
    '''
    면접 일정을 공지하는 채팅 봇
    '''
    room = json.get('room')
    date = kstnow()
    emit('recv_chat', {'title': json.get('title'), 'msg': json.get('msg'), 'user_type': UserType.H2.name, 'date': isoformat(date)}, room=json.get('room_id'))
    db.session.add(Chat(room_id=json.get('room_id'), title=json.get('title'), msg=json.get('msg'), user_type=UserType.H2.name))
    room.status=RoomStatus.S.name
    room.update_room_message(json.get('msg'), date)
    db.session.commit()


@room_token_required
@result_required
@room_writed
@send_alarm
def helper_result(json):
    '''
    면접 결과를 공지하는 채팅 봇
    '''
    room = json.get('room')
    date = kstnow()
    emit('recv_chat', {'title': json.get('title'), 'msg': json.get('msg'), 'user_type': UserType.H3.name, 'date': isoformat(date), 'result': json['result']}, room=json.get('room_id'))
    db.session.add(Chat(room_id=json.get('room_id'), title=json.get('title'), msg=json.get('msg'), user_type=UserType.H3.name, result=json['result']))
    # 면접에 불합격인 사람은 룸상태를 "C" 혹은 "N"으로 변경한다.
    if json['result'] == False:
        if json.get('club').is_recruiting():
            room.status=RoomStatus.N.name
            room.update_room_message(json.get('msg'), date)
        else:    
            room.status=RoomStatus.C.name
            room.update_room_message(json.get('msg'), date)
    # 면접에 합격인 사람은 룸상태를 "R"로 변경한다.
    elif json['result'] == True:
        room.status=RoomStatus.R.name
        room.update_room_message(json.get('msg'), date)
    db.session.commit()


@room_token_required
@answer_required
@room_writed
@send_alarm
def helper_answer(json):
    '''
    면접 결과 응답해주는 채팅 봇
    '''
    room = json.get('room')
    date = kstnow()
    emit('recv_chat', {'title': json.get('title'), 'msg': json.get('msg'), 'user_type': UserType.H4.name, 'date': isoformat(date)}, room=json.get('room_id'))
    db.session.add(Chat(room_id=json.get('room_id'), title=json.get('title'), msg=json.get('msg'), user_type=UserType.H4.name))
    if json.get('answer'):
        db.session.add(ClubMember(user_id=json.get('user_id'), club_id=json.get('club_id')))
        room.status=RoomStatus.C.name
        room.update_room_message(json.get('msg'), date, RoomStatus.name)
    else:
        if json.get('club').is_recruiting():
            room.status=RoomStatus.N.name
            room.update_room_message(json.get('msg'), date, RoomStatus.N.name)
        else:    
            room.status=RoomStatus.C.name
            room.update_room_message(json.get('msg'), date, RoomStatus.C.name)
    
    db.session.commit()


# 소켓 연결
@handshake_jwt_required
def connect(user):
    emit('response', {'msg': 'Socket Connect Successfully'}, namespace='/chat')
    user.session_id = request.sid
    db.session.commit()


# 방 입장
@room_token_required
@room_read
def event_join_room(json):
    join_room(json.get('room_id'))
    emit('response', {'msg': 'Join Room Success'}, namespace='/chat')


# 채팅 보내기
@room_token_required
@chat_message_required
@room_writed
@send_alarm
def event_send_chat(json):
    room = json.get('room')
    date = kstnow()
    emit('recv_chat', {'title': None, 'msg': json.get('msg'), 'user_type': json.get('user_type'), 'date': isoformat(date)}, room=json.get('room_id')) 
    db.session.add(Chat(room_id=json.get('room_id'), msg=json.get('msg'), user_type=json.get('user_type')))
    room.update_room_message(json.get('msg'), date)
    db.session.commit()


# 방 나가기
@room_token_required
@room_read
def event_leave_room(json):
    leave_room(json.get('room_id'))
    emit('response', {'msg': 'Leave Room Success'}, namespace='/chat')


# 지원자 삭제
@room_token_required
@cancel_applicant_required
@room_writed
@send_alarm
def helper_cancel_applicant(json):
    room = json.get('room')
    date = kstnow()
    emit('recv_chat', {'title': json.get('title'), 'msg': json.get('msg'), 'user_type': UserType.H4.name, 'date': isoformat(date)}, room=json.get('room_id'))
    db.session.add(Chat(room_id=json.get('room_id'), title=json.get('title'), msg=json.get('msg'), user_type=UserType.H4.name))
    if json['club'].is_recruiting():
        room.status=RoomStatus.N.name
        room.update_room_message(json.get('msg'), date)
    else:    
        room.status=RoomStatus.C.name
        room.update_room_message(json.get('msg'), date)
    db.session.commit()


# 소켓 연결 끊기
def disconnect():
    pass
