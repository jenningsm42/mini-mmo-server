import struct

from .message import Message


class DisconnectError(Exception):
    pass


class ClientSocket:
    def __init__(self, sock, address):
        self.sock = sock
        self.host = address[0]
        self.port = address[1]
        self.player = None

    def __repr__(self):
        return f'<Client host={self.host} port={self.port}>'

    def fileno(self):
        return self.sock.fileno()

    def close(self):
        self.sock.close()

    # TODO: Make recv, send awaitables - use async sockets
    def recv(self):
        header = self.sock.recv(4)
        if header == b'':
            raise DisconnectError()

        size = struct.unpack('!H', header[2:])[0]
        if size == 0:
            return Message(data=header)

        data = self.sock.recv(size)
        if data == b'':
            raise DisconnectError()

        return Message(data=header+data)

    def send(self, message):
        bytes_sent = self.sock.send(message.data)
        while bytes_sent < len(message.data):
            bytes_sent += self.sock.send(message.data[bytes_sent:])
