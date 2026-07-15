"""
Arman StudioOS

Enterprise Plugin Manager
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# Plugin
# ============================================================

@dataclass(slots=True)
class Plugin:

    name: str

    version: str = "1.0.0"

    enabled: bool = True

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
# Plugin Manager
# ============================================================

class PluginManager:

    def __init__(self):

        self._plugins: Dict[
            str,
            Plugin
        ] = {}

    # ========================================================

    def register(
        self,
        plugin: Plugin
    ):

        self._plugins[
            plugin.name
        ] = plugin

    # ========================================================

    def unregister(
        self,
        name: str
    ):

        self._plugins.pop(
            name,
            None
        )

    # ========================================================

    def enable(
        self,
        name: str
    ):

        if name in self._plugins:

            self._plugins[
                name
            ].enabled = True

    # ========================================================

    def disable(
        self,
        name: str
    ):

        if name in self._plugins:

            self._plugins[
                name
            ].enabled = False

    # ========================================================

    def get(
        self,
        name: str
    ):

        return self._plugins.get(
            name
        )

    # ========================================================

    def installed(self):

        return list(
            self._plugins.values()
        )

    # ========================================================

    def enabled_plugins(self):

        return [

            plugin

            for plugin

            in self._plugins.values()

            if plugin.enabled

        ]

    # ========================================================

    def statistics(self):

        return {

            "installed": len(
                self._plugins
            ),

            "enabled": len(
                self.enabled_plugins()
            ),

            "disabled":

                len(
                    self._plugins
                )

                -

                len(
                    self.enabled_plugins()
                )

        }

    # ========================================================

    def clear(self):

        self._plugins.clear()


# ============================================================
# Singleton
# ============================================================

plugin_manager = PluginManager()