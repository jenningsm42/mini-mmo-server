import socket


class ServerSocket:
    def __init__(self, port=1337):
        self.port = port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(('', self.port))
        self.sock.listen(10)

    def fileno(self):
        return self.sock.fileno()

    def accept(self):
        return self.sock.accept()

    def close(self):
        self.sock.close()
