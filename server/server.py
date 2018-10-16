import asyncio
import logging

from .client import Client, DisconnectError
from .message import Message
from .message_type import MessageType
from .proto.PlayerJoin_pb2 import PlayerLeave
from .service.player import PlayerService
from .service.account import AccountService

logger = logging.getLogger(__name__)


def register_handler(message_type):
    def decorator(func):
        Server.HANDLERS[message_type] = func
        return func
    return decorator


class Server:
    HANDLERS = {}

    def __init__(self, port=1337):
        self.port = port
        self.clients = []

    async def handle_client(self, reader, writer):
        client = Client(reader, writer)
        self.clients.append(client)
        logger.info(f'{client} has connected')

        while True:
            try:
                m = await client.recv()
            except DisconnectError:
                await self.disconnect_user(client, self.broadcast)
                break

            try:
                message_type = MessageType(m.message_type)
            except ValueError:
                logger.info('Received invalid message type %s',
                            m.message_type)
                continue

            handler = Server.HANDLERS.get(message_type)
            if not handler:
                logger.info('No handler for %s', message_type)
                continue

            try:
                await handler(m, client, self.broadcast)
            except DisconnectError:
                await self.disconnect_user(client, self.broadcast)
                break
            except Exception:
                logger.exception('Handler raised exception')

        logger.info(f'{client} has disconnected')
        writer.close()

    async def broadcast(self, message, exclude=None):
        coros = [client.send(message)
                 for client in self.clients
                 if client != exclude]
        await asyncio.gather(*coros)

    async def disconnect_user(self, client, broadcast):
        self.clients.remove(client)

        if client.username is None:
            return

        with AccountService() as service:
            service.logout(client.username)

        if client.player_id is None:
            return

        player_leave_message = PlayerLeave()
        player_leave_message.player_id = client.player_id

        with PlayerService() as service:
            service.remove(client.player_id)

        await self.broadcast(Message(
            message_type=MessageType.player_leave,
            message=player_leave_message),
            exclude=client)
