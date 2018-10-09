import base64
import hashlib

from sqlalchemy.exc import IntegrityError
import bcrypt

from .base import Base
from server.model.account import Account


class AccountNotFoundError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class AccountAlreadyExistsError(Exception):
    pass


class AccountService(Base):
    def create(self, username, password):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if account:
            raise AccountAlreadyExistsError()

        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest())

        account = Account(
            username=username,
            password_hash=bcrypt.hashpw(hashed, bcrypt.gensalt()),
            logged_in=False)

        self.session.add(account)

        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            raise AccountAlreadyExistsError()

    def get(self, username, password):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if not account:
            raise AccountNotFoundError()

        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest())
        if bcrypt.checkpw(hashed, account.password_hash):
            return account

        raise InvalidPasswordError()

    def get_characters(self, username):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if not account:
            raise AccountNotFoundError()

        return account.characters

    def add_character(self, username, character):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if not account:
            raise AccountNotFoundError()

        account.characters.append(character)
        self.session.flush()

        account = self.session.query(Account).filter(
            Account.username == username).first()
        return account.characters[-1].id

    def logout(self, username):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if account:
            account.logged_in = False
