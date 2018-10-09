from sqlalchemy import Boolean, Column, LargeBinary, String
from sqlalchemy.orm import relationship

from .base import Base


class Account(Base):
    __tablename__ = 'accounts'

    username = Column(String, primary_key=True)
    password_hash = Column(LargeBinary, nullable=False)

    logged_in = Column(Boolean, nullable=False)

    characters = relationship('Character')

    def __repr__(self):
        return f'<Account username={self.username}>'
