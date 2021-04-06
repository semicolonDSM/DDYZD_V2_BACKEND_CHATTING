from functools import wraps

def room_writed(fn):
    '''
    요약: 채팅방 읽지 않음 처리 데코레이터
    send_chat, helper_apply, helper_schedule, helper_result에서 사용한다.
    일반 유저가 보낸경우 동아리장이 읽지 않음처리가 되고 동아리장이 보낸 경우엔 그 반대.
    room_read 데코레이터와 처리 방법이 반대다.(헷갈릴 수 있음)
    '''
    @wraps(fn)
    def wrapper(json):
        room = json.get('room')
        room.writed(user_type=json.get('user_type'))

        return fn(json)
    return wrapper