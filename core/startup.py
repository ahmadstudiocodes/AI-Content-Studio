from core.logger import logger
from core.settings import settings

from memory.memory_manager import memory

from core.registry import registry

from agents.general_agent import GeneralAgent
from agents.youtube_agent import YouTubeAgent
from agents.architecture_agent import ArchitectureAgent
from agents.script_agent import ScriptAgent
from agents.thumbnail_agent import ThumbnailAgent

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

    logger.info("Registering Agents...")

    registry.register(
        "general",
        GeneralAgent()
    )

    registry.register(
        "youtube",
        YouTubeAgent()
    )

    registry.register(
        "script",
        ScriptAgent()
    )

    registry.register(
        "thumbnail",
       ThumbnailAgent()
    )

    registry.register(
        "architecture",
        ArchitectureAgent()
    )

    logger.info(f"{registry.count()} Agents Registered")

    logger.info("Registering Providers...")

    provider_manager.register(
        LocalProvider()
    )

    logger.info("Local Provider Registered")

    logger.info("Startup Completed.")