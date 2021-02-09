from asyncio import create_task, wait, FIRST_COMPLETED
from logging import getLogger

from .http_check import run_http_check


logger = getLogger(__name__)


async def run_checks(conf, model):
    tasks = []
    for project in conf.projects:
        for check in project.http_checks:
            tasks.append(create_task(run_http_check(check=check, model=model)))
    done, pending = await wait(tasks, return_when=FIRST_COMPLETED)
