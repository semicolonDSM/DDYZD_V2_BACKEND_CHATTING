from app import websocket as flask_websocket
from flask import Blueprint

api_v1_0 = Blueprint('apiv1.0', __name__)

from .chathelper import *

@api_v1_0.route("/ping")
def ping():
    return {"msg": "ping successfully"}, 200


# chathelper event
flask_websocket.on_event('helper_apply', helper_apply, namespace='/chat')
flask_websocket.on_event('helper_schedule', helper_schedule, namespace='/chat')
flask_websocket.on_event('helper_result', helper_result, namespace='/chat')
flask_websocket.on_event('helper_answer', helper_answer, namespace='/chat')

# websocket event
flask_websocket.on_event('connect', connect, namespace='/chat')
flask_websocket.on_event('disconnect', disconnect, namespace='/chat')
flask_websocket.on_event('join_room', event_join_room, namespace='/chat')
flask_websocket.on_event('leave_room', event_leave_room, namespace='/chat')
flask_websocket.on_event('send_chat', event_send_chat, namespace='/chat')