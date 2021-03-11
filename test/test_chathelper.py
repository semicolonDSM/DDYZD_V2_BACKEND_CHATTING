from app.models import Room
from app import logger
from conftest import room_token
from conftest import jwt_token
from app import websocket
import json


def test_helper_apply(db_setting, flask_websocket, flask_client, flask_app):
    # 웹 소켓 연결
    flask_websocket.emit('join_room', {'room_token': room_token(user_id=1, room_id=3, user_type='C')}, namespace='/chat')
    flask_websocket.emit('helper_apply', {'room_token': room_token(user_id=4, room_id=3, user_type='U'), 'major': '프론트엔드'}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[1]

    assert recv['name'] == 'alarm'
    assert recv['args'][0]['room_id'] != 3

    flask_websocket.emit('helper_apply', {'room_token': room_token(user_id=3, room_id=2, user_type='U'), 'major': '프론트엔드'}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '400: You are already apply to this club' 


def test_helper_schedule(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('join_room', {'room_token': room_token(room_id=2)}, namespace='/chat')
    flask_websocket.emit('helper_schedule', {'date': '2020년 6월 18일 오후 6시 10분', 'location': '3층 그린존','room_token': room_token(room_id=2)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[2]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '안은결님의 면접 일정'
    assert recv['args'][0]['msg'] != None


def test_helper_result(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('join_room', {'room_token': room_token(room_id=2)}, namespace='/chat')
    flask_websocket.emit('helper_result', {'result': True, 'room_token': room_token(room_id=2)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[2]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '안은결님 세미콜론 동아리 합격을 축하드립니다!'
    assert recv['args'][0]['msg'] == '안은결님의 세미콜론 동아리 면접결과, 합격을 알려드립니다'
    assert recv['args'][0]['result'] == True

    flask_websocket.emit('helper_result', {'result': True, 'room_token': room_token(user_type='U')}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '403: Only club head use this helper'


## 방 들어가기 테스트 (채팅 보내기 전에 먼저 실행하자)## 
def test_join_room(flask_websocket, db_setting):
    flask_websocket.emit('join_room', {'room_token': room_token()}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['args'][0]['msg'] == 'Join Room Success'


## 채팅 보내기 테스트 ## 
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


## 방 나가기 테스트 (채팅 보내고 난 뒤에 실행 되어야함!) ## 
def test_leave_room(flask_websocket, db_setting):
    flask_websocket.emit('leave_room', {'room_token': room_token()}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['args'][0]['msg'] == 'Leave Room Success'    


def test_helper_cancel_applicant(db_setting, flask_websocket, flask_client):
    flask_websocket.emit('helper_cancel_applicant', {'room_token': room_token(room_id=3)}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[1]

    assert recv['name'] == 'recv_chat'
    assert recv['args'][0]['date'] != None
    assert recv['args'][0]['title'] == '세미콜론 동아리의 지원이 취소 되었습니다'
    assert recv['args'][0]['msg'] == '성예인님의 동아리 지원이 취소 되었습니다'

    flask_websocket.emit('helper_cancel_applicant', {'room_token': room_token(room_id=3, user_type='C')}, namespace='/chat')
    recv = flask_websocket.get_received(namespace='/chat')[0]

    assert recv['name'] == 'error'
    assert recv['args'][0]['msg'] == '400: User is not applicant or scheduled'
