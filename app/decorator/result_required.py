from app.models.type import FcmType
from app import error
from config import Config
from flask_socketio import emit
from functools import wraps

def get_result_message(user, club, result):
    if result:
        title = "{user}님 {club} 동아리 합격을 축하드립니다!".format(user=user.name, club=club.name)
        msg = "{user}님의 {club} 동아리 면접결과, 합격을 알려드립니다".format(user=user.name, club=club.name)
    else:
        title = "{user}님은 불합격하셨습니다".format(user=user.name)
        msg = "{user}님의 {club} 동아리 면접결과, 불합격을 알려드립니다".format(user=user.name, club=club.name)

    return title, msg    


def result_required(fn):
    '''
    요약: helper_result 동아리 면접 결과 처리하는 데코레이터
    마찬가지로 room_token_required와 같이 연계되어야 한다.
    '''
    @wraps(fn)
    def wrapper(json):
        user = json.get('room').user
        club = json.get('club')
        json['result'] = json.get('args').get('result')
        # 면접 결과가 없는 경우
        if json.get('result') is None:
            return emit('error', error.BadRequest('Please send with result'), namespace='/chat')
        # 동아리 장이 아닌 사람이 호출한 경우
        if json.get('user_type') != 'C':
            return emit('error', error.Forbidden('Only club head use this helper'), namespace='/chat') 
        # 면접 일정을 보내지 않은 사람에게 보낸 경우
        if not user.is_scheduled(club):
            return emit('error', error.BadRequest('The user is not schduled'), namespace='/chat') 

        json['title'], json['msg'] = get_result_message(user, club, json.get('result'))
        json['fcm_type'] = FcmType.H.name # fcm 알림을 보낼 때 사용할 봇이 보낸 메시지임을 알려둠

        return fn(json)
    return wrapper 
