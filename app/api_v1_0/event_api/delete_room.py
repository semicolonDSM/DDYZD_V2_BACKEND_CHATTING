from app.decorator.room_token_required import room_token_required
from app.decorator.room_read import room_read
from flask_socketio import join_room
from flask_socketio import emit

@room_token_required
def event_delete_room(json):
    room = json.get('room')
    room.delete_chats(json.get('user_type'))
