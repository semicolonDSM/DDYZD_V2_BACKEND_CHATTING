from functools import wraps

def room_read(fn):
    '''
    요약: 채팅방 읽음 처리 데코레이터
    join_room, leave_room 이벤트에서 사용한다. 
    '''
    @wraps(fn)
    def wrapper(json):
        room = json.get('room')
        room.read(user_type=json.get('user_type'))

        return fn(json)
    return wrapper
