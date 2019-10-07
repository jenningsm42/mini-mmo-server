from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Chunks_pb2 import ChunkObject, ChunkRequest, ChunkResponse


@register_handler(MessageType.chunk_request)
async def chunk_request(message, client, server):
    info = ChunkRequest()
    info.ParseFromString(message.serialized_message)

    chunk_id = (int(info.chunk_x), int(info.chunk_y))
    chunk = server.map.chunks.get(chunk_id, [])

    response = ChunkResponse()
    response.chunk_x = info.chunk_x
    response.chunk_y = info.chunk_y

    for chunk_object in chunk:
        chunk_object_info = ChunkObject()
        chunk_object_info.object_id = chunk_object.object_id
        chunk_object_info.x = chunk_object.x
        chunk_object_info.y = chunk_object.y

        response.objects.append(chunk_object_info)

    await client.send(Message(
        message_type=MessageType.chunk_response,
        message=response))
