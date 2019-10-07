from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerMove_pb2 import (
    PlayerMove, OtherPlayerMove, PlayerStop, OtherPlayerStop)
from server.service.player import PlayerService
from server.util.vector import Vector


@register_handler(MessageType.player_move)
async def player_move(message, client, server):
    info = PlayerMove()
    info.ParseFromString(message.serialized_message)

    with PlayerService() as service:
        player = service.get(client.player_id)
        if not player:
            raise Exception('Received player_move event for invalid player!')

        character = player.character
        character.set_position_synchronized(server.map, Vector(info.x, info.y))

        # We sometimes get numbers like 1e-5, so set them to zero to reduce
        # long running errors
        clean_velocity = Vector(info.velocity_x, info.velocity_y)
        clean_velocity.clear_zero_values()
        character.velocity_x = clean_velocity.x
        character.velocity_y = clean_velocity.y

    server.players.update_character(client, character)

    broadcast_message = OtherPlayerMove()
    broadcast_message.player_id = client.player_id
    broadcast_message.x = character.last_x
    broadcast_message.y = character.last_y
    broadcast_message.velocity_x = character.velocity_x
    broadcast_message.velocity_y = character.velocity_y

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
        character.set_position_synchronized(server.map, Vector(info.x, info.y))
        character.velocity_x = 0
        character.velocity_y = 0

    server.players.update_character(client, character)

    broadcast_message = OtherPlayerStop()
    broadcast_message.player_id = client.player_id
    broadcast_message.x = character.last_x
    broadcast_message.y = character.last_y

    await server.broadcast(Message(
        message_type=MessageType.other_player_stop,
        message=broadcast_message),
        exclude=client)
