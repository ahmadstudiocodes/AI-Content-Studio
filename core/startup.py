from core.logger import logger
from core.settings import settings


def startup():

    logger.info("Studio Starting...")

    settings.load()

    logger.info("Startup Finished.")