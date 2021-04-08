from conftest import room_token

# 방 나가기 테스트 (채팅 보내고 난 뒤에 실행 되어야함!)
def test_leave_room(flask_websocket, db_setting):
    flask_websocket.emit('leave_room', {'room_token': room_token()}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['args'][0]['msg'] == 'Leave Room Success'    
