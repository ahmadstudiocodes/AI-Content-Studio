# core/events.py
# Part 90
# EventBus Enterprise Monitoring Dashboard and Observability Layer

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from .middleware import (
    EventMiddleware,
)
# ============================================================
# Observability Signal Type
# ============================================================


class EventObservabilitySignal(str, Enum):
    """
    Monitoring signal categories.
    """

    METRIC = "metric"

    LOG = "log"

    TRACE = "trace"

    ALERT = "alert"



# ============================================================
# Dashboard Widget Type
# ============================================================


class EventDashboardWidgetType(str, Enum):
    """
    Dashboard visualization types.
    """

    COUNTER = "counter"

    GRAPH = "graph"

    STATUS = "status"

    TABLE = "table"



# ============================================================
# Observability Record
# ============================================================


@dataclass(slots=True)
class EventObservabilityRecord:
    """
    Single observability data point.
    """

    signal:      EventObservabilitySignal

    name: str

    value: Any

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Dashboard Widget
# ============================================================


@dataclass(slots=True)
class EventDashboardWidget:
    """
    Dashboard component.
    """

    name: str

    widget_type:      EventDashboardWidgetType

    source: str

    description: str



# ============================================================
# Metrics Collector
# ============================================================


class EventMetricsCollector:
    """
    Collects runtime metrics.

    Tracks:
    - Events
    - Errors
    - Latency
    - Throughput
    """

    def __init__(
        self,
    ) -> None:

        self.records: list[
            EventObservabilityRecord
        ] = []



    def record(
        self,
        name:
            str,
        value:
            Any,
    ) -> None:

        self.records.append(
            EventObservabilityRecord(
                signal=
                    EventObservabilitySignal.METRIC,

                name=
                    name,

                value=
                    value,
            )
        )



    def latest(
        self,
    ) -> list[
        EventObservabilityRecord
    ]:

        return self.records[-100:]



# ============================================================
# Trace Collector
# ============================================================


class EventTraceCollector:
    """
    Distributed tracing layer.
    """

    def __init__(
        self,
    ) -> None:

        self.traces: list[
            Dict[str, Any]
        ] = []



    def start(
        self,
        operation:
            str,
    ) -> str:

        trace_id = (
            uuid.uuid4()
            .hex
        )


        self.traces.append(
            {

                "trace_id":
                    trace_id,

                "operation":
                    operation,

                "start":
                    datetime.now(UTC),

            }
        )


        return trace_id



    def finish(
        self,
        trace_id:
            str,
    ) -> None:

        for trace in self.traces:

            if (
                trace["trace_id"]
                ==
                trace_id
            ):

                trace["end"] = (
                    datetime.now(UTC)
                )



# ============================================================
# Alert Engine
# ============================================================


class EventAlertEngine:
    """
    Detects abnormal conditions.
    """

    def __init__(
        self,
    ) -> None:

        self.alerts: list[
            Dict[str, Any]
        ] = []



    def trigger(
        self,
        name:
            str,
        message:
            str,
    ) -> None:

        self.alerts.append(
            {

                "name":
                    name,

                "message":
                    message,

                "time":
                    datetime.now(UTC),

            }
        )



# ============================================================
# Dashboard Manager
# ============================================================


class EventMonitoringDashboard:
    """
    Enterprise observability dashboard.

    Includes:
    - Metrics
    - Traces
    - Alerts
    - Widgets
    """

    def __init__(
        self,
    ) -> None:

        self.widgets: list[
            EventDashboardWidget
        ] = []

        self.metrics = (
            EventMetricsCollector()
        )

        self.traces = (
            EventTraceCollector()
        )

        self.alerts = (
            EventAlertEngine()
        )



    def add_widget(
        self,
        widget:
            EventDashboardWidget,
    ) -> None:

        self.widgets.append(
            widget
        )



    def overview(
        self,
    ) -> Dict[str, Any]:

        return {

            "widgets":
                len(
                    self.widgets
                ),

            "metrics":
                len(
                    self.metrics.records
                ),

            "alerts":
                len(
                    self.alerts.alerts
                ),

            "traces":
                len(
                    self.traces.traces
                ),

        }



# ============================================================
# Default Dashboard Setup
# ============================================================


class EventDefaultDashboardBuilder:
    """
    Creates standard production dashboard.
    """

    def build(
        self,
        dashboard:
            EventMonitoringDashboard,
    ) -> None:


        dashboard.add_widget(
            EventDashboardWidget(
                name=
                    "Event Throughput",

                widget_type=
                    EventDashboardWidgetType.GRAPH,

                source=
                    "metrics.events_per_second",

                description=
                    "Events processed per second",
            )
        )


        dashboard.add_widget(
            EventDashboardWidget(
                name=
                    "System Health",

                widget_type=
                    EventDashboardWidgetType.STATUS,

                source=
                    "health.status",

                description=
                    "Current system state",
            )
        )


        dashboard.add_widget(
            EventDashboardWidget(
                name=
                    "Errors",

                widget_type=
                    EventDashboardWidgetType.COUNTER,

                source=
                    "metrics.errors",

                description=
                    "Total runtime errors",
            )
        )



# ============================================================
# Observability Middleware
# ============================================================


class EventObservabilityMiddleware(
    EventMiddleware
):
    """
    Monitoring integration layer.
    """

    def __init__(
        self,
        dashboard:
            EventMonitoringDashboard,
    ) -> None:

        super().__init__(
            "observability"
        )

        self.dashboard = dashboard



# ============================================================
# Global Observability Objects
# ============================================================


event_monitoring_dashboard = (
    EventMonitoringDashboard()
)


EventDefaultDashboardBuilder().build(
    event_monitoring_dashboard
)


event_observability_middleware = (
    EventObservabilityMiddleware(
        event_monitoring_dashboard
    )
)