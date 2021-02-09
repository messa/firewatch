from aiohttp import ClientSession, ClientError
from asyncio import sleep
from collections import namedtuple
from datetime import datetime
from logging import getLogger
from random import random
from time import monotonic as monotime


logger = getLogger(__name__)

HTTPCheckResult = namedtuple('HTTPCheckResult', 'time duration_headers total_duration status_ok error')


async def run_http_check(check, model):
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
    async with ClientSession() as session:
        start_time = datetime.utcnow()
        mt0 = monotime()
        try:
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
                return HTTPCheckResult(
                    time=start_time,
                    duration_headers=mt1 - mt0,
                    total_duration=mt2 - mt0,
                    status_ok=response.status >= 200 and response.status < 300,
                    error=None)
        except ClientError as e:
            mt2 = monotime()
            logger.info('GET %r raised %r', check.url, e)
            return HTTPCheckResult(
                time=start_time,
                duration_headers=None,
                total_duration=mt2 - mt0,
                status_ok=False,
                error=str(e))
