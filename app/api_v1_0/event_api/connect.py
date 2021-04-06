from app.decorator import handshake_jwt_required
from app import db
from flask_socketio import emit
from flask import request

# 소켓 연결
@handshake_jwt_required
def connect(user, device):
    emit('response', {'msg': 'Socket Connect Successfully'}, namespace='/chat')
    if device == 'mobile':
        user.mobile_session_id = request.sid
    elif device == 'desktop':
        user.desktop_session_id= request.sid
    db.session.commit()