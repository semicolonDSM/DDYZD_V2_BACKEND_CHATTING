from app import websocket as flask_websocket
from flask import Blueprint

api_v1_0 = Blueprint('apiv1.0', __name__)


@api_v1_0.route("/ping")
def ping():
    return {"msg": "ping successfully"}, 200


# chathelper api
from .helper_api.helper_apply import helper_apply
from .helper_api.helper_schedule import helper_schedule
from .helper_api.helper_result import helper_result
from .helper_api.helper_answer import helper_answer
from .helper_api.helper_cancel_applicant import helper_cancel_applicant

flask_websocket.on_event('helper_apply', helper_apply, namespace='/chat')
flask_websocket.on_event('helper_schedule', helper_schedule, namespace='/chat')
flask_websocket.on_event('helper_result', helper_result, namespace='/chat')
flask_websocket.on_event('helper_answer', helper_answer, namespace='/chat')
flask_websocket.on_event('helper_cancel_applicant', helper_cancel_applicant, namespace='/chat')

# event api
from .event_api.connect import connect
from .event_api.join_room import event_join_room
from .event_api.leave_room import event_leave_room
from .event_api.send_chat import event_send_chat
from .event_api.delete_room import event_delete_room

flask_websocket.on_event('connect', connect, namespace='/chat')
flask_websocket.on_event('join_room', event_join_room, namespace='/chat')
flask_websocket.on_event('leave_room', event_leave_room, namespace='/chat')
flask_websocket.on_event('send_chat', event_send_chat, namespace='/chat')
flask_websocket.on_event('delete_room', event_delete_room, namespace='/chat')
