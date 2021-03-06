from datetime import datetime

from server.server import register_handler
from server.message_type import MessageType
from server.message import Message

from server.proto.Characters_pb2 import (
    CharactersResponse, CreateCharacterRequest, CreateCharacterResponse)
from server.service.account import AccountService
from server.model.character import Character


@register_handler(MessageType.characters_request)
async def characters_request(message, client, server):
    response = CharactersResponse()

    with AccountService() as service:
        characters = service.get_characters(client.username)

        for character in characters:
            character_info = response.characters.add()
            character_info.character_id = character.id
            character_info.name = character.name
            character_info.body_color = character.body_color
            character_info.shirt_color = character.shirt_color
            character_info.legs_color = character.legs_color
            character_info.x = character.last_x
            character_info.y = character.last_y

    await client.send(Message(
        message_type=MessageType.characters_response,
        message=response))


@register_handler(MessageType.create_character_request)
async def create_character(message, client, server):
    info = CreateCharacterRequest()
    info.ParseFromString(message.serialized_message)

    character = Character(
        account_username=client.username,
        name=info.name,
        body_color=info.body_color,
        shirt_color=info.shirt_color,
        legs_color=info.legs_color,
        last_x=300,
        last_y=300,
        velocity_x=0,
        velocity_y=0,
        last_position_update=datetime.now())

    response = CreateCharacterResponse()

    with AccountService() as service:
        character_id = service.add_character(client.username, character)

    response.success = True
    response.character_id = character_id
    response.x = character.last_x
    response.y = character.last_y

    await client.send(Message(
        message_type=MessageType.create_character_response,
        message=response))
