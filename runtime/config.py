from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict



@dataclass
class RuntimeConfig:

    name: str = "Arman StudioOS Runtime"

    version: str = "1.0"

    debug: bool = True

    providers: Dict[str, Any] = field(
        default_factory=dict
    )

    features: Dict[str, bool] = field(
        default_factory=dict
    )



class RuntimeConfigManager:
    """
    Runtime configuration controller.
    """


    def __init__(
        self,
        config: RuntimeConfig | None = None
    ):

        self.config = (
            config
            or RuntimeConfig()
        )



    def set_feature(
        self,
        name: str,
        enabled: bool
    ):

        self.config.features[name] = enabled



    def is_enabled(
        self,
        name: str
    ):

        return (
            self.config.features
            .get(
                name,
                False
            )
        )



    def set_provider(
        self,
        name: str,
        settings: Any
    ):

        self.config.providers[name] = settings



    def validate(self):

        return bool(
            self.config.name
            and self.config.version
        )



runtime_config_manager = RuntimeConfigManager()