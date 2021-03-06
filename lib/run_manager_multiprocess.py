import asyncio
import concurrent.futures
from multiprocessing import JoinableQueue
import logging

from lib import settings
from .run_manager import run, start_manager_as_loop
from lib.wrappers.queues import AsyncQueueWrapper

logger = logging.getLogger(settings.LOGGER_NAME)


queue = AsyncQueueWrapper(JoinableQueue())


def start_manager_as_process(stop_event):
    print('STARTING')
    from lib import definitions
    import logging
    settings.POSTFIX = 'manager'
    settings.CONFIG = definitions.CONFIG_CLS(*settings.CONFIG_ARGS)
    settings.CONFIG.configure_logging()
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.info('Starting Message Manager for %s', settings.APP_NAME)
    settings.HOME = settings.CONFIG.home
    settings.DATA_DIR = settings.CONFIG.data_home
    start_manager_as_loop(queue, stop_event)


def start_multiprocess_manager(stop_event) -> asyncio.Task:
    executor = concurrent.futures.ProcessPoolExecutor
    return asyncio.create_task(run(executor, start_manager_as_process, stop_event))


def start_multiprocess_manager2(queue) -> asyncio.Task:
    executor = concurrent.futures.ThreadPoolExecutor
    return asyncio.create_task(run(executor, start_manager_as_process, queue))



