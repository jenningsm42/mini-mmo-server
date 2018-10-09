from .session import Session


class Base:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.expunge_all()
        self.session.close()
