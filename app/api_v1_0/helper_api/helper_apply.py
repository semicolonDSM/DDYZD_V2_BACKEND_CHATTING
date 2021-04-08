from app.decorator.apply_required import apply_required
from app.decorator.room_token_required import room_token_required
from app.decorator.room_writed import room_writed
from app.decorator.send_alarm import send_alarm
from app.models.function import isoformat
from app.models.function import kstnow
from app.models.type import RoomType
from app.models.type import UserType
from app.models.club import Major
from app.models.chat import Chat
from app import db
from flask_socketio import emit

# 동아리 지원
@room_token_required
@apply_required
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
    room.status=RoomType.A.name
    room.update_room_message(json.get('msg'), date)
    db.session.commit()
