from json import dumps

from flask import Flask, request, Response
from pydantic import BaseModel

from microblog.message_service import MessageService, UnknownMessageError
from microblog.models import Message

app = Flask(__name__)
message_service = MessageService()


def respond(status: int, content=None):
    return Response(
        (
            ''
            if status in {204, 304}
            else (
                content.json(indent=2, sort_keys=True)
                if isinstance(content, BaseModel)
                else dumps(content, indent=2, sort_keys=True)
            )
        ),
        status=status,
        content_type='application/json'
    )


def respond_error(status: int, throwable: Exception):
    return respond(status, dict(status=status,
                                error=dict(type=type(throwable).__name__,
                                           message=str(throwable) or None)))


@app.route('/api/messages/', methods=['GET', 'POST'])
def api_messages():
    if request.method == 'GET':
        return respond_error(503, NotImplementedError())
    elif request.method == 'POST':
        inbound_message = request.json()
        message = Message(**inbound_message)
        try:
            return respond(200, message_service.create(message))
        except AssertionError as e:
            return respond_error(400, e)
    else:
        return respond_error(405, RuntimeError('Not supported'))


# noinspection PyShadowingBuiltins
@app.route('/api/messages/<id>', methods=['GET', 'PATCH', 'DELETE'])
def api_message(id: str):
    if request.method == 'GET':
        try:
            return respond(200, message_service.get(id))
        except UnknownMessageError as e:
            return respond_error(404, e)
    elif request.method == 'PATCH':
        inbound_message = request.json()
        message = Message(**inbound_message)
        try:
            return respond(200, message_service.patch(id, message))
        except UnknownMessageError as e:
            return respond_error(404, e)
    elif request.method == 'DELETE':
        message_service.delete(id)
        return respond(204)
    else:
        return respond_error(405, RuntimeError('Not supported'))
