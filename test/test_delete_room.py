from conftest import room_token
from app.models.chat import Room
from app.models.user import User

# 동아리 지원 테스트
def test_delete_room(db_setting, flask_websocket, flask_client, flask_app):
    # 채팅 삭제 테스트
    r = Room.query.get(1).breakdown(User.query.get(2))
    assert r[0]['msg'] == '두번째 채팅'
    assert r[1]['msg'] == '첫번째 채팅'

    flask_websocket.emit('delete_room', {'room_token': room_token(user_id=2, room_id=1, user_type='U')}, namespace='/chat')

    r = Room.query.get(1).breakdown(User.query.get(2))
    assert r == []
    
    r = Room.query.get(1).breakdown(User.query.get(1))
    assert r[0]['msg'] == '두번째 채팅'
    assert r[1]['msg'] == '첫번째 채팅'
