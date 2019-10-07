from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerJoin_pb2 import (
    PlayersResponse, JoinRequest, PlayerJoin)
from server.service.player import PlayerService
from server.service.character import CharacterService


@register_handler(MessageType.join_request)
async def player_join(message, client, server):
    info = JoinRequest()
    info.ParseFromString(message.serialized_message)

    with CharacterService() as service:
        character = service.get(info.character_id)

    with PlayerService() as service:
        character = service.session.merge(character)
        service.create(character)

    server.players.update_all_positions()

    players_response = PlayersResponse()
    for other_character in server.players.characters.values():
        player_info = players_response.players.add()
        player_info.player_id = other_character.id
        player_info.character.x = other_character.last_x
        player_info.character.y = other_character.last_y
        player_info.velocity_x = other_character.velocity_x
        player_info.velocity_y = other_character.velocity_y
        player_info.character.body_color = other_character.body_color
        player_info.character.shirt_color = other_character.shirt_color
        player_info.character.legs_color = other_character.legs_color
        player_info.character.name = other_character.name

    client.player_id = info.character_id
    server.players.add(client, character)

    await client.send(Message(
        message_type=MessageType.players_response,
        message=players_response))

    player_join = PlayerJoin()
    player_join.player_id = client.player_id
    player_join.character.x = character.last_x
    player_join.character.y = character.last_y
    player_join.character.body_color = character.body_color
    player_join.character.shirt_color = character.shirt_color
    player_join.character.legs_color = character.legs_color
    player_join.character.name = character.name

    await server.broadcast(Message(
        message_type=MessageType.player_join,
        message=player_join),
        exclude=client)


@register_handler(MessageType.players_request)
async def players_state(message, client, server):
    if not client.player_id:
        raise Exception('Received players_request event for invalid player!')

    server.players.update_all_positions()

    players_response = PlayersResponse()
    for character in server.players.players.values():
        if character.id == client.player_id:
            continue

        player_info = players_response.players.add()
        player_info.player_id = character.id
        player_info.x = character.last_x
        player_info.y = character.last_y
        player_info.velocity_x = character.velocity_x
        player_info.velocity_y = character.velocity_y

    await client.send(Message(
        message_type=MessageType.players_response,
        message=players_response))
