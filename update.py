from core.logger import logger
from core.backup import create_backup
from database.init_db import initialize


def update():

    logger.info("Updating Project")

    create_backup()

    initialize()

    logger.info("Finished")


if __name__ == "__main__":

    update()