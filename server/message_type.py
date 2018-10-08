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
