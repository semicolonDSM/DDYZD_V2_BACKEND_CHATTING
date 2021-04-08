from conftest import room_token

#  면접 결과 테스트
def test_helper_result(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('join_room', {'room_token': room_token(room_id=3)}, namespace='/chat')
    flask_websocket.emit('helper_result', {'result': True, 'room_token': room_token(room_id=3)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[2]
    
    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '성예인님 세미콜론 동아리 합격을 축하드립니다!'
    assert recv['args'][0]['msg'] == '성예인님의 세미콜론 동아리 면접결과, 합격을 알려드립니다'
    assert recv['args'][0]['result'] == True

    flask_websocket.emit('helper_result', {'result': True, 'room_token': room_token(user_type='U')}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '403: Only club head use this helper'
