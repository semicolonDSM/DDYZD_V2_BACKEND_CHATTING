from app.decorator import schedule_information_required
from app.decorator import room_token_required
from app.decorator import room_writed
from app.decorator import send_alarm
from app.models import RoomStatus
from app.models import UserType
from app.models import Chat
from app.models import isoformat
from app.models import kstnow
from app import db
from flask_socketio import emit

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