from app.decorator.room_token_required import room_token_required
from app.decorator.room_read import room_read
from flask_socketio import join_room
from flask_socketio import emit

@room_token_required
@room_read
def event_join_room(json):
    join_room(json.get('room_id'))
    emit('response', {'msg': 'Join Room Success'}, namespace='/chat')
