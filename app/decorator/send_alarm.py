from app.models import UserType
from app.models import FcmType
from app.fcm import fcm_alarm
from config import Config
from flask_socketio import emit
from functools import wraps

import asyncio



def send_alarm(fn):
    '''
    요약: 알람 보내는 처리를 하는 데코레이터
    send_chat, helper_apply, helper_schedule, helper_result에서 사용한다.
    '''
    @wraps(fn)
    def wrapper(json):
        room = json.get('room')
        #일반 유저가 메시지를 보낸 경우
        if json.get('user_type') == UserType.U.name:
            send_user = room.user
            sender = room.user.name
            recv_user = room.club.club_head[0].user
            user_type = 'C'
        #동아리장이 메시지를 보낸 경우
        else:
            send_user = room.club.club_head[0].user
            sender = room.club.name
            recv_user = room.user
            user_type = 'U'

        # 일반 채팅 메시지인 경우
        if json.get('fcm_type') == FcmType.C.name:
            msg = json.get('msg')
        # 봇이 보낸 메시지인 경우
        else:
            msg = json.get('title')
        
        # 채팅방에 join 하지 않은 경우 fcm과 알람을 보낸다.
        if not recv_user.is_in_room(room):
            asyncio.run(fcm_alarm(sender=sender, msg=msg, token=recv_user.device_token, 
                room_id=room.id, user_type=user_type))
        # title: 보내는 사람 이름 혹은 보내는 동아리 이름
        # msg: 일반 유저인 경우 일반 메시지, 봇인 경우 제목을 전송
        emit_alarm(send_user, recv_user, str(json.get('room_id')))
        
        return fn(json)
    return wrapper

    
def emit_alarm(send_user, recv_user, room_id):
    if recv_user.mobile_session_id is not None:
        emit('alarm', {'room_id': room_id}, room=recv_user.mobile_session_id)
    if recv_user.desktop_session_id is not None:
        emit('alarm', {'room_id': room_id}, room=recv_user.desktop_session_id)
    if send_user.mobile_session_id is not None:
        emit('alarm', {'room_id': room_id}, room=send_user.mobile_session_id)
    if send_user.desktop_session_id is not None:
        emit('alarm', {'room_id': room_id}, room=send_user.desktop_session_id)
