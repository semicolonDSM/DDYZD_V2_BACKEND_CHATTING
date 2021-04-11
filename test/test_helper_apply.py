from conftest import room_token

# 동아리 지원 테스트
def test_helper_apply(db_setting, flask_websocket, flask_client, flask_app):
    # 웹 소켓 연결
    flask_websocket.emit('join_room', {'room_token': room_token(user_id=1, room_id=1, user_type='C')}, namespace='/chat')
    flask_websocket.emit('helper_apply', {'room_token': room_token(user_id=2, room_id=1, user_type='U'), 'major': '프론트엔드'}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[1]

    assert recv['name'] == 'alarm'
    assert recv['args'][0]['room_id'] != 3

    flask_websocket.emit('helper_apply', {'room_token': room_token(user_id=2, room_id=1, user_type='U'), 'major': '프론트엔드'}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '400: You are already apply to this club' 
