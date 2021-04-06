from app.models import FcmType
from app import error
from flask_socketio import emit
from functools import wraps
import jwt

def get_schedule_message(user, club, date, location):
    title = '{user_name}님의 면접 일정'.format(user_name=user.name)
    msg = '''{gcn} {user_name}님의 {club_name} 동아리 면접 일정입니다
    
    일시: {date}
    장소: {location}'''.format(
    gcn=user.gcn, 
    user_name=user.name, 
    club_name=club.name,
    date=date,
    location=location)
    
    return title, msg


def schedule_required(fn):
    '''
    요약: helper_schedule 이벤트에서 일정 정보를 처리하는 데코레이터
    room_token_required과 같이 연계되어 사용되어야한다.
    '''
    @wraps(fn)
    def wrapper(json):
        user = json.get('room').user
        club = json.get('club')
        # 면접 일정이 없는 경우
        if json.get('args').get('date') is None or json.get('args').get('location') is None:
            return emit('error', error.BadRequest('Please send with date and location'), namespace='/chat')
          # 동아리 장이 아닌 사람이 호출한 경우
        if json.get('user_type') != 'C':
            return emit('error', error.Forbidden('Only club head use this helper'), namespace='/chat') 
        # 신청자가 아닌 사용자에게 보낸 경우
        if not user.is_applicant(club):
            return emit('error', error.BadRequest('The user is not applicant'), namespace='/chat') 

        json['title'], json['msg'] = get_schedule_message(user, club, json.get('args').get('date'), json.get('args').get('location'))
        json['fcm_type'] = FcmType.H.name  # fcm 알림을 보낼 때 사용할 봇이 보낸 메시지임을 알려둠
    
        return fn(json)
    return wrapper