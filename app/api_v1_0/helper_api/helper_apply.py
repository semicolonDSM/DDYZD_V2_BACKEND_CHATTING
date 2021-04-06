from app.decorator import apply_message_required
from app.decorator import room_token_required
from app.decorator import room_writed
from app.decorator import send_alarm
from app.models import RoomStatus
from app.models import UserType
from app.models import Major
from app.models import Chat
from app.models import isoformat
from app.models import kstnow
from app import db
from flask_socketio import emit

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
