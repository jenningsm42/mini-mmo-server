from server.server import register_slow_tick_event


@register_slow_tick_event
async def tick_update_positions(server):
    server.players.update_all_positions()
