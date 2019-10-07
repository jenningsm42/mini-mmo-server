from enum import IntEnum


class MessageType(IntEnum):
    version_request = 0
    version_response = 1
    login_request = 2
    login_response = 3
    register_request = 4
    register_response = 5

    player_move = 6
    other_player_move = 7
    player_stop = 8
    other_player_stop = 9
    player_join = 10
    player_leave = 11
    players_request = 12
    players_response = 13
    join_request = 14
    join_response = 15

    characters_request = 16
    characters_response = 17
    create_character_request = 18
    create_character_response = 19

    send_chat_message = 20
    receive_chat_message = 21

    chunk_request = 22
    chunk_response = 23
