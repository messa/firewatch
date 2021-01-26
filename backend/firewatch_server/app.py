from aiohttp.web import Application, AppRunner, TCPSite
from argparse import ArgumentParser
from asyncio import run, sleep
from logging import getLogger

from .views import routes as views_routes


logger = getLogger(__name__)


async def get_app():
    app = Application()
    app.router.add_routes(views_routes)
    return app


def main():
    p = ArgumentParser()
    args = p.parse_args()
    setup_logging()
    run(async_main(args=args))


def setup_logging():
    from logging import DEBUG, basicConfig
    basicConfig(level=DEBUG, format='%(asctime)s %(name)-25s %(levelname)5s: %(message)s')


async def async_main(args):
    app = await get_app()
    runner = AppRunner(app)
    await runner.setup()
    bind_host = ''
    bind_port = 8000
    site = TCPSite(runner, bind_host, bind_port)
    await site.start()
    logger.info('Listening in %s:%s', bind_host, bind_port)
    while True:
        # https://github.com/aio-libs/aiohttp/blob/master/aiohttp/web.py#L347-L348 :)
        await sleep(3600)
    await runner.cleanup()
