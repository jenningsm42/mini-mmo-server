from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from .base import Base
from .account import Account
from .player import Player


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    account_username = Column(String(256), ForeignKey(Account.username))
    player_id = Column(Integer, ForeignKey(Player.id))

    name = Column(String(256), nullable=False)
    color = Column(Integer, nullable=False)

    last_x = Column(Float, nullable=False)
    last_y = Column(Float, nullable=False)
    velocity_x = Column(Float, nullable=False)
    velocity_y = Column(Float, nullable=False)
    last_position_update = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Character id={self.id} name={self.name}>'

    def get_position(self):
        now = datetime.now()
        delta = (now - self.last_position_update).total_seconds()
        self.last_x = self.last_x + self.velocity_x * delta
        self.last_y = self.last_y + self.velocity_y * delta
        self.last_position_update = now
        return self.last_x, self.last_y
