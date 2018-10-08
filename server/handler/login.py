from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Login_pb2 import LoginRequest, LoginResponse
from server.proto.PlayerJoin_pb2 import PlayerJoin
from server.state.account import AccountNotFoundError, InvalidPasswordError


@register_handler(MessageType.login_request)
async def login(message, client, state, broadcast):
    request = LoginRequest()
    request.ParseFromString(message.serialized_message)

    response = LoginResponse()

    try:
        state.accounts.get_account(request.username, request.password)
    except AccountNotFoundError:
        response.success = False
        response.error_message = 'Invalid username'
    except InvalidPasswordError:
        response.success = False
        response.error_message = 'Invalid password'
    else:
        response.success = True
        player = state.players.create_player()
        client.player = player

        player_join_message = PlayerJoin()
        player_join_message.player_id = player.player_id
        player_join_message.x = 300
        player_join_message.y = 300

        await broadcast(Message(
            message_type=MessageType.player_join,
            message=player_join_message),
            exclude=client)

    client.send(Message(
        message_type=MessageType.login_response,
        message=response))
