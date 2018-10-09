import asyncio
import logging

from sqlalchemy import create_engine
import click

from .model.base import Base
from .server import Server
from .service.session import Session


@click.command()
@click.option('-p', '--port', default=1337)
@click.option('-v', '--verbose', is_flag=True)
@click.option('--db', default='sqlite:////tmp/foobar.db')
def main(port, verbose, db):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    engine = create_engine(db)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = Server(port=port)
    logging.info('Running')
    try:
        asyncio.run(s.run())
    except Exception:
        logging.exception('Stopped')
        s.close()


if __name__ == '__main__':
    main()
