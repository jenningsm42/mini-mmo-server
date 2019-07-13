from datetime import datetime
import asyncio
import logging

from server.server import register_slow_tick_event

logger = logging.getLogger(__name__)

KEEP_ALIVE_DURATION = 600


@register_slow_tick_event
async def tick_keep_alive(server):
    # Disconnect players after some amount of inactivity
    now = datetime.now()
    coros = []
    for client, _ in server.players:
        if client.disconnecting:
            continue

        last_message_duration = (
            now - client.last_message_time).total_seconds()

        if last_message_duration > KEEP_ALIVE_DURATION:
            logger.info('{client} has gone past keep alive duration')
            coros.append(server.disconnect_user(client))

    if coros:
        await asyncio.gather(*coros)
