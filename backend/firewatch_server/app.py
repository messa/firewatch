from aiohttp.web import Application, AppRunner, TCPSite
from argparse import ArgumentParser
from asyncio import run, sleep, create_task, wait, FIRST_COMPLETED
import hashlib
from logging import getLogger, Formatter
import re

from .configuration import Configuration
from .checks import run_checks
from .model import Model
from .auth import routes as auth_routes
from .views import routes as views_routes


logger = getLogger(__name__)

log_format = '%(asctime)s %(shortName)-30s %(levelname)5s: %(message)s'


async def get_app(conf, model):
    app = Application()
    app['conf'] = conf
    app['model'] = model
    app.router.add_routes(auth_routes)
    app.router.add_routes(views_routes)
    from aiohttp_session import setup as aiohttp_session_setup
    from aiohttp_session.cookie_storage import EncryptedCookieStorage
    secret_key = hashlib.sha256(conf.session_secret_bytes).digest()
    aiohttp_session_setup(app, EncryptedCookieStorage(secret_key))
    return app


def main():
    p = ArgumentParser()
    p.add_argument('--bind', help='address to bind to (default: all interfaces)')
    p.add_argument('--port', type=int, help='port to listen to')
    p.add_argument('--conf', help='path to configuration file')
    args = p.parse_args()
    setup_logging()
    conf = Configuration(args=args)
    run(async_main(conf=conf))


def setup_logging():
    from logging import DEBUG, StreamHandler
    getLogger('').setLevel(DEBUG)
    h = StreamHandler()
    h.setFormatter(CustomFormatter(log_format))
    h.setLevel(DEBUG)
    getLogger('').addHandler(h)


class CustomFormatter (Formatter):

    def formatMessage(self, record):
        assert not hasattr(record, 'shortName')
        record.shortName = re.sub(r'^firewatch_server\.', '.', record.name)
        return super().formatMessage(record)


async def async_main(conf):
    model = Model()
    tasks = [
        create_task(run_web(conf=conf, model=model)),
        create_task(run_checks(conf=conf, model=model)),
    ]
    done, pending = await wait(tasks, return_when=FIRST_COMPLETED)


async def run_web(conf, model):
    app = await get_app(conf=conf, model=model)
    runner = AppRunner(app)
    await runner.setup()
    try:
        site = TCPSite(runner, conf.bind_host, conf.bind_port)
        await site.start()
        logger.info('Listening in %s:%s', conf.bind_host, conf.bind_port)
        while True:
            # the same usage as in https://github.com/aio-libs/aiohttp/blob/master/aiohttp/web.py
            await sleep(3600)
    finally:
        await runner.cleanup()
