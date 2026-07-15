# core/events.py
# Part 88
# EventBus Final Documentation Package and Architecture Diagram Metadata

from __future__ import annotations

import json
import threading
import time
import uuid

from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Callable, Optional
from .core import EventMiddleware

# ============================================================
# Documentation Package Version
# ============================================================


class EventDocumentationPackageVersion(str, Enum):
    """
    Documentation release versions.
    """

    V1 = "1.0.0"

    V1_1 = "1.1.0"

    V2 = "2.0.0"



# ============================================================
# Architecture Layer Type
# ============================================================


class EventArchitectureLayer(str, Enum):
    """
    EventBus architecture layers.
    """

    API = "api"

    CORE = "core"

    PROCESSING = "processing"

    INFRASTRUCTURE = "infrastructure"

    SECURITY = "security"

    INTEGRATION = "integration"



# ============================================================
# Architecture Node
# ============================================================


@dataclass(slots=True)
class EventArchitectureNode:
    """
    Architecture diagram component.
    """

    name: str

    layer:     EventArchitectureLayer

    description: str

    dependencies: list[str] = field(
        default_factory=list
    )



# ============================================================
# Architecture Diagram Metadata
# ============================================================


@dataclass(slots=True)
class EventArchitectureDiagram:
    """
    Complete architecture map.
    """

    title: str

    nodes: list[
        EventArchitectureNode
    ]

    version:      EventDocumentationPackageVersion



# ============================================================
# Diagram Builder
# ============================================================


class EventArchitectureDiagramBuilder:
    """
    Generates architecture metadata.
    """

    def build(
        self,
    ) -> EventArchitectureDiagram:

        nodes = [

            EventArchitectureNode(
                name=
                    "Developer SDK",

                layer=
                    EventArchitectureLayer.API,

                description=
                    "External developer interface",

                dependencies=[
                    "Public API"
                ],
            ),


            EventArchitectureNode(
                name=
                    "Enterprise EventBus",

                layer=
                    EventArchitectureLayer.CORE,

                description=
                    "Central event routing engine",

                dependencies=[
                    "Middleware",
                    "Queue",
                ],
            ),


            EventArchitectureNode(
                name=
                    "Priority Queue",

                layer=
                    EventArchitectureLayer.PROCESSING,

                description=
                    "High performance event processing",

                dependencies=[
                    "Worker Pool"
                ],
            ),


            EventArchitectureNode(
                name=
                    "Security Layer",

                layer=
                    EventArchitectureLayer.SECURITY,

                description=
                    "Encryption and key management",

                dependencies=[
                    "Policy Engine"
                ],
            ),


            EventArchitectureNode(
                name=
                    "Integration Layer",

                layer=
                    EventArchitectureLayer.INTEGRATION,

                description=
                    "Workspace Runtime Plugin bridges",

                dependencies=[
                    "Event Bridges"
                ],
            ),


            EventArchitectureNode(
                name=
                    "Infrastructure",

                layer=
                    EventArchitectureLayer.INFRASTRUCTURE,

                description=
                    "Backup Monitoring Recovery",

                dependencies=[
                    "Health System"
                ],
            ),

        ]


        return EventArchitectureDiagram(
            title=
                "Arman StudioOS Enterprise Event Architecture",

            nodes=
                nodes,

            version=
                EventDocumentationPackageVersion.V1,
        )



# ============================================================
# Documentation Exporter
# ============================================================


class EventDocumentationPackageExporter:
    """
    Creates documentation package.
    """

    def export(
        self,
        diagram:
            EventArchitectureDiagram,
    ) -> Dict[str, Any]:

        return {

            "title":
                diagram.title,

            "version":
                diagram.version.value,

            "layers":
                [
                    node.layer.value
                    for node
                    in diagram.nodes
                ],

            "components":
                [
                    node.name
                    for node
                    in diagram.nodes
                ],

        }



# ============================================================
# Developer Reference Package
# ============================================================


class EventDeveloperReferencePackage:
    """
    Complete developer documentation.

    Includes:
    - Architecture map
    - API reference
    - Component list
    """

    def __init__(
        self,
    ) -> None:

        self.diagram_builder = (
            EventArchitectureDiagramBuilder()
        )

        self.exporter = (
            EventDocumentationPackageExporter()
        )



    def generate(
        self,
    ) -> Dict[str, Any]:

        diagram = (
            self.diagram_builder.build()
        )


        return self.exporter.export(
            diagram
        )



# ============================================================
# Documentation Middleware
# ============================================================


class EventArchitectureDocumentationMiddleware(
    EventMiddleware
):
    """
    Architecture documentation layer.
    """

    def __init__(
        self,
        package:
            EventDeveloperReferencePackage,
    ) -> None:

        super().__init__(
            "architecture_documentation"
        )

        self.package = package



# ============================================================
# Global Documentation Objects
# ============================================================


event_developer_reference_package = (
    EventDeveloperReferencePackage()
)


event_architecture_documentation = (
    event_developer_reference_package.generate()
)


event_architecture_documentation_middleware = (
    EventArchitectureDocumentationMiddleware(
        event_developer_reference_package
    )
)