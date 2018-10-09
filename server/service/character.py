from datetime import datetime

from .base import Base
from server.model.character import Character


class CharacterService(Base):
    def create(self, account, name):
        character = Character(
            account_username=account.username,
            name=name,
            last_x=300,
            last_y=300,
            velocity_x=0,
            velocity_y=0,
            last_position_update=datetime.now())

        self.session.add(character)

    def get(self, character_id):
        return self.session.query(Character).filter(
            Character.id == character_id).first()
