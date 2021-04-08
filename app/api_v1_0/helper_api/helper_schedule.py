from app.decorator.schedule_required import schedule_required
from app.decorator.room_token_required import room_token_required
from app.decorator.room_writed import room_writed
from app.decorator.send_alarm import send_alarm
from app.models.function import isoformat
from app.models.function import kstnow
from app.models.type import RoomType
from app.models.type import UserType
from app.models.chat import Chat
from app import db
from flask_socketio import emit

# 면접 스케쥴 
@room_token_required
@schedule_required
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
    room.status=RoomType.S.name
    room.update_room_message(json.get('msg'), date)
    db.session.commit()