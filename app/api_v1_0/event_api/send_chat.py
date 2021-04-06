from app.decorator import room_token_required
from app.decorator import chat_message_required
from app.decorator import room_writed
from app.decorator import send_alarm
from app.models import Chat
from app.models import isoformat
from app.models import kstnow
from app import db
from flask_socketio import emit

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