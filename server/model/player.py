from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .base import Base


# Table of characters currently loaded into the game
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    character = relationship('Character', uselist=False)
