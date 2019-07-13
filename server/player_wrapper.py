from datetime import datetime


class PlayerWrapper:
    def __init__(self, character):
        self.character = character

    @property
    def last_position(self):
        return self.character.last_x, self.character.last_y

    def update_position(self, now=None):
        vx = self.character.velocity_x
        vy = self.character.velocity_y
        if vx == 0 and vy == 0:
            return

        now = now or datetime.now()
        delta = (now - self.character.last_position_update).total_seconds()

        x = self.character.last_x
        y = self.character.last_y

        self.character.last_x = x + vx * delta
        self.character.last_y = y + vy * delta
        self.character.last_position_update = now

    def set_position(self, position):
        self.character.last_x = position[0]
        self.character.last_y = position[1]
        self.character.last_position_update = datetime.now()
