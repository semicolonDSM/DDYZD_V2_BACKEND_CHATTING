from app.models.type import FcmType
from app import error
from flask_socketio import emit
from functools import wraps


def get_answer_message(user, club, answer):
    if answer:
        title = "{name}님이 동아리원이 되었습니다".format(name=user.name)
        msg = "{club} 동아리원이 되신 것을 진심으로 축하드립니다".format(club=club.name)
    else:
        title = "{name}님이 동아리원을 거절했습니다".format(name=user.name)
        msg = "우린 서로 좋은 인연이 아니였나봐요... 다음에 봐요;"

    return title, msg 


def answer_required(fn):
    '''
    요약: helper_answer 동아리 가입 수락 처리하는 데코레이터
    room_token required로 랩핑 됩니다.
    '''
    @wraps(fn)
    def wrapper(json):
        user = json.get('room').user
        club = json.get('club')
        json['answer'] = json.get('args').get('answer')
        
        # 면접 대답이 없는 경우
        if json.get('answer') is None:
            return emit('error', error.BadRequest('Please send with answer'), namespace='/chat')
        # 면접 결과를 받지 않은 사람의 경우
        if not user.is_resulted(club):
            return emit('error', error.BadRequest('The user is not resulted'), namespace='/chat') 

        json['title'], json['msg'] = get_answer_message(user, club, json.get('answer'))
        json['fcm_type'] = FcmType.H.name # fcm 알림을 보낼 때 사용할 봇이 보낸 메시지임을 알려둠

        return fn(json)
    return wrapper
