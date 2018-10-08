from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerJoin_pb2 import PlayersResponse


@register_handler(MessageType.players_request)
async def players_state(message, client, state, broadcast):
    players_response = PlayersResponse()

    for player in state.players.players.values():
        if player.player_id == client.player.player_id:
            break
        player_info = players_response.players.add()
        player_info.player_id = player.player_id
        x, y = player.get_position()
        player_info.x = x
        player_info.y = y
        player_info.velocity_x = player.velocity_x
        player_info.velocity_y = player.velocity_y

    client.send(Message(
        message_type=MessageType.players_response,
        message=players_response))
