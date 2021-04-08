from app.models.type import FcmType
from app import error
from flask_socketio import emit
from functools import wraps

def chat_required(fn):    
    '''
    요약: 채팅 메시지 처리 데코레이터
    채팅시 메시지를 처리해주는 데코레이터다(에러 처리 및 전처리 포함)
    send_chat에서 사용한다.
    '''
    @wraps(fn)
    def wrapper(json):
        json['msg'] = json.get('args').get('msg')
        if json.get('msg') is None:
            return emit('error', error.BadRequest('Please send with message'), namespace='/chat')
        json['fcm_type'] = FcmType.C.name # fcm 알림을 보낼 때  일반 채팅 메시지 임을 알려둠
        
        return fn(json)
    return wrapper
