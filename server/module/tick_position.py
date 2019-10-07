from server.server import register_fast_tick_event

from server.service.character import CharacterService


@register_fast_tick_event
async def tick_update_positions(server):
    server.players.update_all_positions()

    with CharacterService() as service:
        for _, character in server.players:
            service.session.merge(character)
