from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Register_pb2 import RegisterRequest, RegisterResponse
from server.state.account import AccountAlreadyExistsError


@register_handler(MessageType.register_request)
async def register_account(message, client, state, broadcast):
    request = RegisterRequest()
    request.ParseFromString(message.serialized_message)

    response = RegisterResponse()

    try:
        state.accounts.create_account(request.username, request.password)
    except AccountAlreadyExistsError:
        response.success = False
        response.error_message = 'Username already in use'
    else:
        response.success = True

    client.send(Message(
        message_type=MessageType.register_response,
        message=response))
