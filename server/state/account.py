import base64
import hashlib

import bcrypt


class AccountNotFoundError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class AccountAlreadyExistsError(Exception):
    pass


class Account:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


class Accounts:
    def __init__(self):
        # Maps username to account
        self.accounts = {}

    def get_account(self, username, password):
        account = self.accounts.get(username)
        if not account:
            raise AccountNotFoundError()

        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest())
        if bcrypt.checkpw(hashed, account.password_hash):
            return account

        raise InvalidPasswordError()

    def create_account(self, username, password):
        if self.accounts.get(username):
            raise AccountAlreadyExistsError()

        hashed = base64.b64encode(hashlib.sha256(password.encode()).digest())
        self.accounts[username] = Account(
            username,
            bcrypt.hashpw(hashed, bcrypt.gensalt()))
