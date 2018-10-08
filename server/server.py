import asyncio
import concurrent.futures
import logging
import select

from .client_socket import ClientSocket, DisconnectError
from .message import Message
from .message_type import MessageType
from .proto.PlayerJoin_pb2 import PlayerLeave
from .server_socket import ServerSocket
from .server_state import ServerState

logger = logging.getLogger(__name__)


def register_handler(message_type):
    def decorator(func):
        Server.HANDLERS[message_type] = func
        return func
    return decorator


def run_handler(coro):
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coro)
    finally:
        loop.close()


class Server:
    HANDLERS = {}

    def __init__(self, port=1337):
        self.port = port
        self.clients = []
        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.sock = ServerSocket(port=self.port)
        self.state = ServerState()

    async def run(self):
        while True:
            ready_to_read, ready_to_write, _ = select.select(
                [self.sock] + self.clients, self.clients, [], 60)

            for s in ready_to_read:
                if type(s) == ServerSocket:
                    conn, address = s.accept()
                    self.clients.append(ClientSocket(conn, address))
                    logger.info(f'{self.clients[-1]} connected')
                elif type(s) == ClientSocket:
                    try:
                        m = s.recv()
                        try:
                            message_type = MessageType(m.message_type)
                        except ValueError:
                            logger.info('Received invalid message type %s',
                                        m.message_type)
                            break

                        handler = Server.HANDLERS.get(message_type)
                        if handler:
                            try:
                                await asyncio.get_event_loop().run_in_executor(
                                    self.executor,
                                    run_handler,
                                    handler(m, s,
                                            self.state,
                                            self.get_broadcast()))
                            except Exception:
                                logger.exception('Exception in handler')
                        else:
                            logger.info('No handler for %s!', m)
                    except DisconnectError:
                        logger.info(f'{s} disconnected')
                        await asyncio.get_event_loop().run_in_executor(
                            self.executor,
                            run_handler,
                            self.disconnect_player(s, self.get_broadcast()))
                        s.close()
                        self.clients.remove(s)

    def get_broadcast(self):
        async def broadcast(message, exclude=None):
            for client in self.clients:
                if client != exclude:
                    client.send(message)
        return broadcast

    async def disconnect_player(self, client, broadcast):
        if client.player is None:
            return

        player_leave_message = PlayerLeave()
        player_leave_message.player_id = client.player.player_id

        self.state.players.remove_player(client.player.player_id)

        await broadcast(Message(
            message_type=MessageType.player_leave,
            message=player_leave_message),
            exclude=client)

    def close(self):
        self.sock.close()
        self.executor.shutdown()
