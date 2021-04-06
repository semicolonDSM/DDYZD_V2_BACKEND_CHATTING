from app.decorator.room_token_required import room_token_required
from app.decorator.room_read import room_read
from flask_socketio import leave_room
from flask_socketio import emit

# 방 나가기
@room_token_required
@room_read
def event_leave_room(json):
    leave_room(json.get('room_id'))
    emit('response', {'msg': 'Leave Room Success'}, namespace='/chat')
