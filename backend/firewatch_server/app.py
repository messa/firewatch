from aiohttp.web import Application, AppRunner, TCPSite
from argparse import ArgumentParser
from asyncio import run, sleep, create_task, wait, FIRST_COMPLETED
from collections import namedtuple
from datetime import datetime
import hashlib
from logging import getLogger
from random import random
from time import monotonic as monotime

from .configuration import Configuration
from .model import Model
from .auth import routes as auth_routes
from .views import routes as views_routes


logger = getLogger(__name__)


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
    from logging import DEBUG, basicConfig
    basicConfig(level=DEBUG, format='%(asctime)s %(name)-30s %(levelname)5s: %(message)s')


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


async def run_checks(conf, model):
    tasks = []
    for project in conf.projects:
        for check in project.http_checks:
            tasks.append(create_task(run_check(check=check, model=model)))
    done, pending = await wait(tasks, return_when=FIRST_COMPLETED)


async def run_check(check, model):
    await sleep(random()) # do not start everything at once
    while True:
        logger.debug('run_check: %r', check)
        try:
            result = await perform_check(check)
        except Exception as e:
            logger.exception('perform_check(%r) failed: %r', check, e)
        else:
            logger.debug('result: %r', result)
            await model.store_check_result(check, result)
        await sleep(check.interval)


async def perform_check(check):
    from aiohttp import ClientSession
    async with ClientSession() as session:
        start_time = datetime.utcnow()
        mt0 = monotime()
        async with session.get(check.url) as response:
            mt1 = monotime()
            content = await response.read()
            mt2 = monotime()
            logger.debug('response.status: %r', response.status)
            logger.debug('response.headers: %r', response.headers)
            if len(content) <= 100:
                logger.debug('response content: %r', content)
            else:
                logger.debug('response content: %r...', content[:120])
            return CheckResult(
                time=start_time,
                duration_headers=mt1 - mt0,
                total_duration=mt2 - mt0,
                status_ok=response.status >= 200 and response.status < 300)


CheckResult = namedtuple('CheckResult', 'time duration_headers total_duration status_ok')
