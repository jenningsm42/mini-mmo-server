from collections import defaultdict
from datetime import datetime
import asyncio
import logging
import uuid

from .client import Client, DisconnectError
from .message import Message
from .message_type import MessageType
from .player_collection import PlayerCollection
from .proto.PlayerJoin_pb2 import PlayerLeave
from .service.account import AccountService
from .service.player import PlayerService

logger = logging.getLogger(__name__)


def register_handler(message_type):
    def decorator(func):
        Server.HANDLERS[message_type] = func
        return func
    return decorator


def register_slow_tick_event(func):
    Server.TICK_EVENTS[Server.SLOW_TICK_DELAY].append(func)
    return func


class Server:
    HANDLERS = {}
    TICK_EVENTS = defaultdict(list)

    SLOW_TICK_DELAY = 500

    def __init__(self, port=1337):
        self.port = port
        self.clients = []
        self.players = PlayerCollection()

    async def tick(self, delay):
        """ Run registered tick events every delay milliseconds """
        while True:
            coros = [event(self) for event in Server.TICK_EVENTS[delay]]
            await asyncio.gather(*coros)
            await asyncio.sleep(delay / 1000)

    async def handle_client(self, reader, writer):
        client = Client(reader, writer, uuid.uuid4())
        self.clients.append(client)
        logger.info(f'{client} has connected')

        while True:
            try:
                m = await client.recv()
            except DisconnectError:
                await self.disconnect_user(client)
                break

            client.set_last_message_time(datetime.now())

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
                await handler(m, client, self)
            except DisconnectError:
                try:
                    await self.disconnect_user(client)
                except Exception:
                    logger.exception('Exception while disconnecting user')
                break
            except Exception:
                logger.exception('Handler raised exception')

        logger.info(f'{client} has disconnected')
        writer.close()

    async def broadcast(self, message, exclude=None):
        """" Broadcasts given message to all connected clients """
        coros = [client.send(message)
                 for client in self.clients
                 if client != exclude]
        await asyncio.gather(*coros)

    async def broadcast_in_range(self, message, center, radius, exclude=None):
        """ Broadcasts given message to players within the given range """
        coros = [client.send(message)
                 for client in self.players.get_players_in_range(
                     center, radius)
                 if client != exclude]
        await asyncio.gather(*coros)

    async def disconnect_user(self, client):
        if client.disconnecting:
            return

        client.disconnecting = True

        client.writer.close()
        self.clients.remove(client)

        # Never logged in - no need to log out
        if client.username is None:
            return

        self.players.remove(client)

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
            message=player_leave_message))
