from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Chat_pb2 import (
    SendChatMessage, ReceiveChatMessage)
from server.service.player import PlayerService

CHAT_RADIUS = 200


@register_handler(MessageType.send_chat_message)
async def send_chat_message(message, client, server):
    info = SendChatMessage()
    info.ParseFromString(message.serialized_message)

    broadcast_message = ReceiveChatMessage()
    broadcast_message.player_id = client.player_id
    broadcast_message.msg = info.msg

    with PlayerService() as service:
        player = service.get(client.player_id)
        position = player.character.last_x, player.character.last_y

    await server.broadcast_in_range(Message(
        message_type=MessageType.receive_chat_message,
        message=broadcast_message),
        position,
        CHAT_RADIUS)
