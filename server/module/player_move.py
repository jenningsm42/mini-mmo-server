from datetime import datetime

from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerMove_pb2 import (
    PlayerMove, OtherPlayerMove, PlayerStop, OtherPlayerStop)
from server.service.player import PlayerService
from server.player_wrapper import PlayerWrapper


@register_handler(MessageType.player_move)
async def player_move(message, client, server):
    info = PlayerMove()
    info.ParseFromString(message.serialized_message)

    with PlayerService() as service:
        player = service.get(client.player_id)
        if not player:
            raise Exception('Received player_move event for invalid player!')

        character = player.character
        character.last_x = info.x
        character.last_y = info.y
        character.velocity_x = info.velocity_x
        character.velocity_y = info.velocity_y
        character.last_position_update = datetime.now()

    server.players.update_player(client, PlayerWrapper(character))

    broadcast_message = OtherPlayerMove()
    broadcast_message.player_id = client.player_id
    broadcast_message.x = info.x
    broadcast_message.y = info.y
    broadcast_message.velocity_x = info.velocity_x
    broadcast_message.velocity_y = info.velocity_y

    await server.broadcast(Message(
        message_type=MessageType.other_player_move,
        message=broadcast_message),
        exclude=client)


@register_handler(MessageType.player_stop)
async def player_stop(message, client, server):
    info = PlayerStop()
    info.ParseFromString(message.serialized_message)

    with PlayerService() as service:
        player = service.get(client.player_id)
        if not player:
            raise Exception('Received player_stop event for invalid player!')

        character = player.character
        character.last_x = info.x
        character.last_y = info.y
        character.velocity_x = 0
        character.velocity_y = 0
        character.last_position_update = datetime.now()

    server.players.update_player(client, PlayerWrapper(character))

    broadcast_message = OtherPlayerStop()
    broadcast_message.player_id = client.player_id
    broadcast_message.x = info.x
    broadcast_message.y = info.y

    await server.broadcast(Message(
        message_type=MessageType.other_player_stop,
        message=broadcast_message),
        exclude=client)
