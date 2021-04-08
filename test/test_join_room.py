from conftest import room_token

# 방 들어가기 테스트 (채팅 보내기 전에 먼저 실행하자)
def test_join_room(flask_websocket, db_setting):
    flask_websocket.emit('join_room', {'room_token': room_token()}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['args'][0]['msg'] == 'Join Room Success'
