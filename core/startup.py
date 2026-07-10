from core.logger import logger
from core.settings import settings

from memory.memory_manager import memory

from core.registry import registry

from core.agent_loader import agent_loader

from providers.provider_manager import provider_manager
from providers.local_provider import LocalProvider


def startup():

    logger.info("=" * 40)
    logger.info("Booting Arman StudioOS")
    logger.info("=" * 40)

    logger.info("Loading Settings...")
    settings.load()

    logger.info("Loading Memory...")

    if memory:
        logger.info("Memory Ready")

    logger.info("Loading Agents...")

    agent_loader.load()

    logger.info(f"{registry.count()} Agents Registered")

    logger.info("Registering Providers...")

    provider_manager.register(
        LocalProvider()
    )

    logger.info("Local Provider Registered")

    logger.info("Startup Completed.")