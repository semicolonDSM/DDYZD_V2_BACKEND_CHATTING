from conftest import room_token

# 면접 스케줄 할당 테스트
def test_helper_schedule(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('join_room', {'room_token': room_token(room_id=2)}, namespace='/chat')
    flask_websocket.emit('helper_schedule', {'date': '2020년 6월 18일 오후 6시 10분', 'location': '3층 그린존','room_token': room_token(room_id=2)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[2]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '안은결님의 면접 일정'
    assert recv['args'][0]['msg'] != None