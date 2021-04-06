from app.models import FcmType
from app import error
from flask_socketio import emit
from functools import wraps

def get_cancel_applicant_message(user, club):
    title = "{club} 동아리의 지원이 취소 되었습니다".format(club=club.name)
    msg = "{name}님의 동아리 지원이 취소 되었습니다".format(name=user.name)

    return title, msg


def cancel_applicant_required(fn):
    '''
    요약: 지원자 삭제하는 데코레이터
    삭제시 메시지와 권한 필터링
    '''
    @wraps(fn)
    def wrapper(json):
        user = json.get('room').user
        club = json.get('club')
        # 동아리 장이 아닌 경우
        if json.get('user_type') != 'C':
            return emit('error', error.Forbidden('You are not a head for the club'), namespace='/chat')
        # 동아리의 지원자가 아닌 경우
        if not (user.is_applicant(club) or user.is_scheduled(club) or user.is_resulted(club)):
            return emit('error', error.BadRequest('User is not applicant or scheduled'), namespace='/chat')

        json['title'], json['msg'] = get_cancel_applicant_message(user, club)
        json['fcm_type'] = FcmType.H.name # fcm 알림을 보낼 때 사용할 봇이 보낸 메시지임을 알려둠

        return fn(json)
    return wrapper
    