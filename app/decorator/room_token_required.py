from app.models.chat import Room
from app.models.user import User
from app.models.club import Club
from config import Config
from flask_socketio import emit
from functools import wraps
from app import error
import jwt

    

def room_token_required(fn):
    '''
    요약: 채팅방 토큰을 요구하는 데코레이터
    send_chat, join_room, leave_room,
    helper_apply, helper_schedule, helper_result에 사용한다.
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = args[0].get('room_token')
        try:
            json = jwt.decode(token, Config.ROOM_SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return emit('error', error.Unauthorized('ExpiredSignatureError'), namespace='/chat')
        except Exception:
            return emit('error', error.Unauthorized(), namespace='/chat')

        json['args'] = args[0] # 나머지 argument는 처리하지 않고 'args' 키에 담아 넘겨준다
        json['club'] = Club.query.get(json.get('club_id'))
        json['user'] = User.query.get(json.get('user_id'))
        json['room'] = Room.query.get(json.get('room_id'))

        return fn(json)
    return wrapper
