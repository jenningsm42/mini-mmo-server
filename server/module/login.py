from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Login_pb2 import LoginRequest, LoginResponse
from server.service.account import (
    AccountService, AccountNotFoundError, InvalidPasswordError)
from server.service.player import PlayerService


@register_handler(MessageType.login_request)
async def login(message, client, server):
    request = LoginRequest()
    request.ParseFromString(message.serialized_message)

    response = LoginResponse()

    with AccountService() as service:
        try:
            account = service.get(request.username, request.password)
        except (AccountNotFoundError, InvalidPasswordError):
            response.success = False
            response.error_message = 'Invalid credentials'
        else:
            response.success = True
            client.username = account.username
            account.logged_in = True

    if response.success:
        with PlayerService() as service:
            account = service.session.merge(account)
            for character in account.characters:
                service.remove(character.id)

    await client.send(Message(
        message_type=MessageType.login_response,
        message=response))
