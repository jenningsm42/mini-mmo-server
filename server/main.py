import asyncio
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
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

    delay = 5
    while True:
        try:
            Base.metadata.create_all(engine)
        except OperationalError:
            logging.error(
                'Could not connect to database, retrying in %s seconds',
                delay)
            time.sleep(delay)
            delay *= 1.5
        else:
            break

    s = Server(port=port)
    logging.info('Running')
    try:
        asyncio.run(s.run())
    except Exception:
        logging.exception('Stopped')
        s.close()


if __name__ == '__main__':
    main()
