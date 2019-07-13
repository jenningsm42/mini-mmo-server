from datetime import datetime
import struct

from .message import Message


class DisconnectError(Exception):
    pass


class Client:
    def __init__(self, reader, writer, uuid):
        self.reader = reader
        self.writer = writer
        self.hash = uuid.int
        self.host, self.port = writer.get_extra_info('peername')
        self.username = None
        self.player_id = None
        self.last_message_time = datetime.now()
        self.disconnecting = False

    def __repr__(self):
        return f'<Client host={self.host} port={self.port}>'

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return other is not None and self.hash == other.hash

    def set_last_message_time(self, time):
        self.last_message_time = time

    async def recv(self):
        if self.reader.at_eof():
            raise DisconnectError()

        header = await self.reader.read(4)
        if not header:
            raise DisconnectError()

        size = struct.unpack('!H', header[2:])[0]
        if size == 0:
            return Message(data=header)

        data = await self.reader.read(size)
        if not data:
            raise DisconnectError()

        return Message(data=header+data)

    async def send(self, message):
        self.writer.write(message.data)
        try:
            await self.writer.drain()
        except BrokenPipeError:
            raise DisconnectError()
