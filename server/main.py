from concurrent.futures import CancelledError
import asyncio
import logging
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import click

from .model.base import Base
from .server import Server
from .service.session import Session


async def serve(port, dry_run):
    s = Server()
    server = await asyncio.start_server(
        s.handle_client, '127.0.0.1', port)

    async with server:
        logging.info('Running')
        try:
            if not dry_run:
                await server.serve_forever()
        except CancelledError:
            logging.info('Stopped')
        except Exception:
            logging.exception('Stopped')
        else:
            logging.info('Stopped')


@click.command()
@click.option('-p', '--port', default=1337)
@click.option('-v', '--verbose', is_flag=True)
@click.option('--db', default='sqlite:////tmp/foobar.db')
@click.option('--dry-run', is_flag=True)
def main(port, verbose, db, dry_run):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    engine = create_engine(db)
    Session.configure(bind=engine)

    delay = 5
    tries = 5
    rate = 1.5
    while True:
        try:
            Base.metadata.create_all(engine)
        except OperationalError:
            if delay >= 5 * rate**tries:
                logging.error('Could not connect to database, terminating')
                sys.exit(1)

            logging.error(
                'Could not connect to database, retrying in %s seconds',
                delay)
            time.sleep(delay)
            delay *= rate
        else:
            break

    asyncio.run(serve(port, dry_run))


if __name__ == '__main__':
    main()
