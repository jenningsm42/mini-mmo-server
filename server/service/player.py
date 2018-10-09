from .base import Base
from server.model.player import Player


class PlayerService(Base):
    def create(self, character):
        player = Player(
            id=character.id,
            character=character)
        self.session.add(player)

    def get(self, character_id):
        return self.session.query(Player).filter(
            Player.id == character_id).first()

    def get_all(self):
        return self.session.query(Player).all()

    def remove(self, character_id):
        # Does nothing on failure
        player = self.session.query(Player).filter(
            Player.id == character_id).first()
        if player:
            self.session.delete(player)
