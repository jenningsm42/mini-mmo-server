from datetime import datetime


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.last_x = 300
        self.last_y = 300
        self.last_position_update = datetime.now()
        self.velocity_x = 0
        self.velocity_y = 0

    def __repr__(self):
        return f'<Player id={self.player_id}>'

    def get_position(self):
        now = datetime.now()
        delta = (now - self.last_position_update).total_seconds()
        self.last_x = self.last_x + self.velocity_x * delta
        self.last_y = self.last_y + self.velocity_y * delta
        self.last_position_update = now
        return self.last_x, self.last_y


class Players:
    def __init__(self):
        # Maps player id to player
        self.players = {}
        self.next_id = 0

    def create_player(self):
        p = Player(self.next_id)
        self.players[self.next_id] = p
        self.next_id += 1
        return p

    def get_player(self, player_id):
        return self.players.get(player_id)

    def remove_player(self, player_id):
        if self.players.get(player_id):
            del self.players[player_id]
