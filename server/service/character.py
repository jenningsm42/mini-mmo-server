from .base import Base
from server.model.character import Character


class CharacterService(Base):
    def get(self, character_id):
        return self.session.query(Character).filter(
            Character.id == character_id).first()
