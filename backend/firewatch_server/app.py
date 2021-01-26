from aiohttp.web import Application, AppRunner, TCPSite
from argparse import ArgumentParser
from asyncio import run, sleep
from logging import getLogger

from .configuration import Configuration
from .views import routes as views_routes


logger = getLogger(__name__)


async def get_app(conf):
    app = Application()
    app['http_checks'] = conf.http_checks
    app.router.add_routes(views_routes)
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
    from logging import DEBUG, basicConfig
    basicConfig(level=DEBUG, format='%(asctime)s %(name)-30s %(levelname)5s: %(message)s')


async def async_main(conf):
    app = await get_app(conf=conf)
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
