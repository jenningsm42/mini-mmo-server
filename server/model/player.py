from sqlalchemy import Column, ForeignKey, Integer

from .base import Base
from .character import Character


# Table of characters currently loaded into the game
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, ForeignKey(Character.id), primary_key=True)
