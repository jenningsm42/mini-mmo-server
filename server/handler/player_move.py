from datetime import datetime

from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerMove_pb2 import (
    PlayerMove, OtherPlayerMove, PlayerStop, OtherPlayerStop)


@register_handler(MessageType.player_move)
async def player_move(message, client, state, broadcast):
    info = PlayerMove()
    info.ParseFromString(message.serialized_message)

    client.player.last_x = info.current_x
    client.player.last_y = info.current_y
    client.player.velocity_x = info.velocity_x
    client.player.velocity_y = info.velocity_y
    client.player.last_position_update = datetime.now()

    broadcast_message = OtherPlayerMove()
    broadcast_message.player_id = client.player.player_id
    broadcast_message.starting_x = info.current_x
    broadcast_message.starting_y = info.current_y
    broadcast_message.velocity_x = info.velocity_x
    broadcast_message.velocity_y = info.velocity_y

    await broadcast(Message(
        message_type=MessageType.other_player_move,
        message=broadcast_message),
        exclude=client)


@register_handler(MessageType.player_stop)
async def player_stop(message, client, state, broadcast):
    info = PlayerStop()
    info.ParseFromString(message.serialized_message)

    client.player.last_x = info.stopped_x
    client.player.last_y = info.stopped_y
    client.player.velocity_x = 0
    client.player.velocity_y = 0
    client.player.last_position_update = datetime.now()

    broadcast_message = OtherPlayerStop()
    broadcast_message.player_id = client.player.player_id
    broadcast_message.stopped_x = info.stopped_x
    broadcast_message.stopped_y = info.stopped_y

    await broadcast(Message(
        message_type=MessageType.other_player_stop,
        message=broadcast_message),
        exclude=client)
