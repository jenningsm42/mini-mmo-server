from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.PlayerJoin_pb2 import (
    PlayersResponse, JoinRequest, PlayerJoin)
from server.service.player import PlayerService
from server.service.character import CharacterService
from server.player_wrapper import PlayerWrapper


@register_handler(MessageType.join_request)
async def player_join(message, client, server):
    info = JoinRequest()
    info.ParseFromString(message.serialized_message)

    with CharacterService() as service:
        character = service.get(info.character_id)

    with PlayerService() as service:
        players = service.get_all()
        characters = [player.character for player in players]
        character = service.session.merge(character)
        service.create(character)

    client.player_id = info.character_id
    server.players.add(client, PlayerWrapper(character))

    players_response = PlayersResponse()

    for other_character in characters:
        pw = PlayerWrapper(other_character)
        pw.update_position()

        player_info = players_response.players.add()
        player_info.player_id = other_character.id
        x, y = pw.last_position
        player_info.character.x = x
        player_info.character.y = y
        player_info.velocity_x = other_character.velocity_x
        player_info.velocity_y = other_character.velocity_y
        player_info.character.body_color = other_character.body_color
        player_info.character.shirt_color = other_character.shirt_color
        player_info.character.legs_color = other_character.legs_color
        player_info.character.name = other_character.name

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

    players_response = PlayersResponse()

    with PlayerService() as service:
        players = service.get_all()

    for player in players:
        if player.id == client.player_id:
            continue

        character = player.character
        pw = PlayerWrapper(character)
        pw.update_position()

        player_info = players_response.players.add()
        player_info.player_id = player.id
        x, y = pw.last_position
        player_info.x = x
        player_info.y = y
        player_info.velocity_x = character.velocity_x
        player_info.velocity_y = character.velocity_y

    await client.send(Message(
        message_type=MessageType.players_response,
        message=players_response))
