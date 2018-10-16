import struct

from .message import Message


class DisconnectError(Exception):
    pass


class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.host, self.port = writer.get_extra_info('peername')
        self.username = None
        self.player_id = None

    def __repr__(self):
        return f'<Client host={self.host} port={self.port}>'

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
