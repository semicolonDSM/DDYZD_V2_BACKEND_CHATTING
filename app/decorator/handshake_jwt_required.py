from app.models.user import User
from config import Config
from flask_socketio import emit
from functools import wraps
from flask import request
import jwt


def handshake_jwt_required(fn):
    '''
    요약: 핸드쉐이크시 jwt 토큰 인증하는 데코레이터
    Web의 경우 Authorization 헤더를 보낼 수 없기 때문에 url query로 토큰을 보낸다.
    하지만 앱(안드로이드, iOS)의 경우에는 헤더에서 토큰을 받는다.
    '''
    @wraps(fn)
    def wrapper():
        device = None
        try:
            if request.args.get('token'):
                token = request.args.get('token') 
                device = 'desktop'
            else:
                token = request.headers.get('Authorization')[7:]
                device = 'mobile'
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return {"msg": "ExpiredSignatureError"}, 401
        except Exception:
            return {"msg": "Unauthorized Header"}, 401
        user = User.query.get_or_404(payload.get('sub'))

        return fn(user, device)
    return wrapper