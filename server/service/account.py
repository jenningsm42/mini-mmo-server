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

        print(hashed)
        account = Account(
            username=username,
            password_hash=bcrypt.hashpw(hashed, bcrypt.gensalt()),
            logged_in=False)
        print(account.password_hash)

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

        print(account.password_hash)
        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest())
        if bcrypt.checkpw(hashed, account.password_hash):
            return account

        raise InvalidPasswordError()

    def logout(self, username):
        account = self.session.query(Account).filter(
            Account.username == username).first()
        if account:
            account.logged_in = False
