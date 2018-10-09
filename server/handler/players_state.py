from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerJoin_pb2 import PlayersResponse
from server.service.player import PlayerService


@register_handler(MessageType.players_request)
async def players_state(message, client, broadcast):
    if not client.player_id:
        raise Exception('Received players_request event for invalid player!')

    players_response = PlayersResponse()

    with PlayerService() as service:
        players = service.get_all()

    for player in players:
        if player.id == client.player_id:
            continue

        character = player.character

        player_info = players_response.players.add()
        player_info.player_id = player.id
        x, y = character.get_position()
        player_info.x = x
        player_info.y = y
        player_info.velocity_x = character.velocity_x
        player_info.velocity_y = character.velocity_y

    client.send(Message(
        message_type=MessageType.players_response,
        message=players_response))
