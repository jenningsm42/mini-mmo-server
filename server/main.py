import asyncio
import logging

import click

from .server import Server


@click.command()
@click.option('-p', '--port', default=1337)
@click.option('-v', '--verbose', is_flag=True)
def main(port, verbose):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    s = Server(port=port)
    logging.info('Running')
    try:
        asyncio.run(s.run())
    except Exception:
        logging.exception('Stopped')
        s.close()


if __name__ == '__main__':
    main()
