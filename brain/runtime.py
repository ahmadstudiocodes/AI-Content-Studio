"""
Arman StudioOS

Enterprise Runtime
"""

from __future__ import annotations

import threading
import time

from brain.scheduler import scheduler
from brain.event_bus import event_bus
from brain.plugin_manager import plugin_manager


class Runtime:

    """
    Central Runtime
    """

    TICK_RATE = 0.05

    def __init__(self):

        self.running = False

        self.thread = None

    # =====================================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._loop,

            daemon=True

        )

        self.thread.start()

    # =====================================================

    def stop(self):

        self.running = False

        if self.thread:

            self.thread.join()

    # =====================================================

    def _loop(self):

        while self.running:

            scheduler.tick()

            event_bus.dispatch()

            time.sleep(
                self.TICK_RATE
            )

    # =====================================================

    def install_plugin(
        self,
        plugin
    ):

        plugin_manager.register(
            plugin
        )

        if hasattr(
            plugin,
            "register"
        ):

            plugin.register(
                event_bus
            )

    # =====================================================

    def uninstall_plugin(
        self,
        name
    ):

        plugin_manager.unregister(
            name
        )

    # =====================================================

    def statistics(self):

        return {

            "running":
                self.running,

            "scheduler":
                scheduler.pending(),

            "plugins":
                plugin_manager.statistics(),

            "events":
                event_bus.statistics()

        }


runtime = Runtime()