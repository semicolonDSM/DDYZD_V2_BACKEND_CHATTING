from app.decorator import room_token_required
from app.decorator import result_required
from app.decorator import room_writed
from app.decorator import send_alarm
from app.models import RoomStatus
from app.models import UserType
from app.models import Chat
from app.models import isoformat
from app.models import kstnow
from app import db
from flask_socketio import emit

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