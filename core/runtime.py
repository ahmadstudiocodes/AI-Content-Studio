from core.task_queue import task_queue
from core.logger import logger


class Runtime:

    def __init__(self):

        self.running = False

    def start(self):

        self.running = True

        logger.info("Runtime Started")

    def stop(self):

        self.running = False

        logger.info("Runtime Stopped")


runtime = Runtime()