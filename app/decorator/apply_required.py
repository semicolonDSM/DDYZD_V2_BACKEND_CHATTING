from app.models import FcmType
from app import error
from config import Config
from flask_socketio import emit
from functools import wraps

def get_apply_message(user, club, major):
    title = '{name}님이 동아리에 지원하셨습니다'.format(name=user.name) 
    msg = '{gcn} {name}님이 {club}에 {major} 분야로 지원하셨습니다'\
        .format(gcn=user.gcn, name=user.name, club=club.name, major=major)
    
    return title, msg


def apply_required(fn):
    '''
    요약: 동아리 지원 메시지 처리 데코레이터
    동아리 지원시 메시지를 처리해주는 데코레이터다(에러 처리 및 전처리 포함)
    helper_apply에서 사용한다.
    '''
    @wraps(fn)
    def wrapper(json):
        user = json.get('user')
        club = json.get('club')
        json['major'] = json.get('args').get('major')
        # 지원하는 전공이 없는 경우
        if json.get('major') is None:
            return emit('error', error.BadRequest('Please send with major'), namespace='/chat')
        # 일반 유저가 아닌 사람이 사용한 경우인지
        if json.get('user_type') != 'U':
            return emit('error', error.BadRequest('Only common user use this helper'), namespace='/chat') 
        # 동아리 지원 진행중인 경우
        if user.is_applicant(club) or user.is_scheduled(club) or user.is_resulted(club):
            return emit('error', error.BadRequest('You are already apply to this club'), namespace='/chat')
        # 동아리에 이미 가입한 경우인지
        if user.is_club_member(club):
            return emit('error', error.BadRequest('You are already member of this club'), namespace='/chat')
        # 동아리 지원 기간이 아닌 경우인지
        if not club.is_recruiting():
            return emit('error', error.BadRequest('Club is not recruiting now!'), namespace='/chat')
        # 동아리가 모집하는 분야가 아닐 때 경우인지
        if json.get('major') is None:
            return emit('error', error.BadRequest('Club does not need '+str(json.get('major'))), namespace='/chat')
    
        json['title'], json['msg'] = get_apply_message(user, club, json.get('major'))
        json['fcm_type'] = FcmType.H.name  # fcm 알림을 보낼 때 사용할 봇이 보낸 메시지임을 알려둠

        return fn(json)
    return wrapper