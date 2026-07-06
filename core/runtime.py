from core.task_queue import task_queue

from core.logger import logger


class Runtime:

    def __init__(self):

        self.running = False

    def start(self):

        self.running = True

        logger.info("Runtime Started")

        while self.running:

            task = task_queue.pop()

            if task is None:

                break

            logger.info(task.name)

    def stop(self):

        self.running = False

        logger.info("Runtime Stopped")


runtime = Runtime()