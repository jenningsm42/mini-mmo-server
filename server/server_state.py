from .state.account import Accounts
from .state.player import Players


class ServerState:
    def __init__(self):
        self.accounts = Accounts()
        self.players = Players()
