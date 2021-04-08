from conftest import room_token

# 채팅 보내기 테스트 
def test_send_chat(db_setting, flask_websocket):
    # 동아리장 채팅
    flask_websocket.emit('join_room', {'room_token': room_token()}, namespace='/chat')
    flask_websocket.emit('send_chat',{'msg': 'Hello \U0001f600', 'room_token': room_token()}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[2]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['msg'] == 'Hello \U0001f600'
    assert recv['args'][0]['user_type'] == 'C'
    assert recv['args'][0]['date'] != None

    # 동아리원 채팅
    flask_websocket.emit('send_chat', {'msg': 'World!', 'room_token': room_token(user_id=2, user_type='U')}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'alarm'
    assert recv['args'][0]['room_id'] == '1'