from app.decorator.room_token_required import room_token_required
from app.decorator.answer_required import answer_required
from app.decorator.room_writed import room_writed
from app.decorator.send_alarm import send_alarm
from app.models.function import isoformat
from app.models.function import kstnow
from app.models.type import RoomType
from app.models.type import UserType
from app.models.club import ClubMember
from app.models.chat import Chat
from app import db
from flask_socketio import emit

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
        room.status=RoomType.C.name
        room.update_room_message(json.get('msg'), date)
    else:
        if json.get('club').is_recruiting():
            room.status=RoomType.N.name
            room.update_room_message(json.get('msg'), date)
        else:    
            room.status=RoomType.C.name
            room.update_room_message(json.get('msg'), date)
    
    db.session.commit()