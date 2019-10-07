from datetime import datetime
from math import sqrt
import logging

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from .base import Base
from .account import Account
from .player import Player
from server.util.aabb import AABB
from server.util.vector import Vector

logger = logging.getLogger(__name__)


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    account_username = Column(String(256), ForeignKey(Account.username))
    player_id = Column(Integer, ForeignKey(Player.id))

    name = Column(String(256), nullable=False)
    body_color = Column(Integer, nullable=False)
    shirt_color = Column(Integer, nullable=False)
    legs_color = Column(Integer, nullable=False)

    last_x = Column(Float, nullable=False)
    last_y = Column(Float, nullable=False)
    velocity_x = Column(Float, nullable=False)
    velocity_y = Column(Float, nullable=False)
    last_position_update = Column(DateTime, nullable=False)

    # AABB dimensions
    WIDTH = 50
    HEIGHT = 40

    DESYNC_DISTANCE_SQUARED = 100  # <= 10 units is ok - trust the client then

    def __repr__(self):
        return f'<Character id={self.id} name={self.name}>'

    @property
    def last_position(self):
        return Vector(self.last_x, self.last_y)

    @property
    def last_velocity(self):
        return Vector(self.velocity_x, self.velocity_y)

    @property
    def aabb(self):
        return AABB(
            self.last_x - Character.WIDTH / 2,
            self.last_y - Character.HEIGHT,
            Character.WIDTH,
            Character.HEIGHT)

    def update_position(self, world, now=None):
        if self.last_velocity.is_zero():
            return

        now = now or datetime.now()
        delta = (now - self.last_position_update).total_seconds()

        position = world.handle_collision(
            self.last_position,
            self.last_velocity * delta,
            self.aabb)

        self.set_position(position, now)

    def set_position(self, position, now=None):
        now = now or datetime.now()

        self.last_x = position.x
        self.last_y = position.y
        self.last_position_update = now

    def set_position_synchronized(self, world, new_position):
        '''
        Set the character's position to the given position if it's not too
        far from the calculated position, else set it to the calculated
        position
        '''
        now = datetime.now()
        self.update_position(world, now)
        distance_squared = self.last_position.distance_squared(new_position)

        if distance_squared > Character.DESYNC_DISTANCE_SQUARED:
            # TODO: Create message to force player in server position
            #       Right now we're (wrongly) trusting the client
            self.set_position(new_position, now)
            distance = sqrt(distance_squared)
            logger.debug(
                f'{self} position desynced by {distance} units!\n' +
                f'Given position:      {new_position}\n' +
                f'Calculated position: {self.last_position}')
            return

        self.set_position(new_position, now)
