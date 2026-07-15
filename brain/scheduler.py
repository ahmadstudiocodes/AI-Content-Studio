"""
Arman StudioOS

Enterprise Scheduler
"""

from __future__ import annotations

import heapq
import threading
import time

from dataclasses import dataclass, field
from typing import Callable, List, Optional


# ============================================================
# Scheduled Task
# ============================================================

@dataclass(order=True)
class ScheduledTask:

    run_at: float

    callback: Callable = field(compare=False)

    interval: Optional[float] = field(
        default=None,
        compare=False
    )

    repeat: bool = field(
        default=False,
        compare=False
    )

    enabled: bool = field(
        default=True,
        compare=False
    )


# ============================================================
# Scheduler
# ============================================================

class Scheduler:

    def __init__(self):

        self._tasks: List[
            ScheduledTask
        ] = []

        self._lock = threading.RLock()

    # ========================================================

    def schedule(
        self,
        delay: float,
        callback: Callable
    ):

        task = ScheduledTask(

            run_at=time.time() + delay,

            callback=callback

        )

        with self._lock:

            heapq.heappush(
                self._tasks,
                task
            )

        return task

    # ========================================================

    def schedule_interval(
        self,
        interval: float,
        callback: Callable
    ):

        task = ScheduledTask(

            run_at=time.time() + interval,

            callback=callback,

            interval=interval,

            repeat=True

        )

        with self._lock:

            heapq.heappush(
                self._tasks,
                task
            )

        return task

    # ========================================================

    def tick(self):

        now = time.time()

        while True:

            with self._lock:

                if not self._tasks:

                    return

                if self._tasks[0].run_at > now:

                    return

                task = heapq.heappop(
                    self._tasks
                )

            if not task.enabled:

                continue

            task.callback()

            if task.repeat:

                task.run_at = (
                    time.time()
                    + task.interval
                )

                with self._lock:

                    heapq.heappush(
                        self._tasks,
                        task
                    )

    # ========================================================

    def cancel(
        self,
        task: ScheduledTask
    ):

        task.enabled = False

    # ========================================================

    def clear(self):

        with self._lock:

            self._tasks.clear()

    # ========================================================

    def pending(self):

        return len(
            self._tasks
        )


# ============================================================
# Singleton
# ============================================================

scheduler = Scheduler()