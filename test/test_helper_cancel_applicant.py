from conftest import room_token

# 지원자 삭제 테스트
def test_helper_cancel_applicant(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('helper_cancel_applicant', {'room_token': room_token(room_id=1)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[1]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '세미콜론 동아리의 지원이 취소 되었습니다'
    assert recv['args'][0]['msg'] == '조호원님의 동아리 지원이 취소 되었습니다'

    flask_websocket.emit('helper_cancel_applicant', {'room_token': room_token(room_id=1, user_type='C')}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '400: User is not applicant or scheduled'
