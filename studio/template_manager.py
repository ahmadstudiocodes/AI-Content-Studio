# ============================================================
# File: studio/template_manager.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import json
import threading
import uuid

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Protocol


class SupportsWorkspace(Protocol):

    @property
    def root(self) -> Path: ...

    @property
    def workspace_id(self) -> str: ...


class SupportsEventBus(Protocol):

    def publish(
        self,
        event: str,
        **payload: Any,
    ) -> None: ...


class SupportsSharedState(Protocol):

    def set(
        self,
        key: str,
        value: Any,
    ) -> None: ...

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any: ...


class SupportsRuntime(Protocol):

    def is_running(
        self,
    ) -> bool: ...


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


class TemplateType(str, Enum):

    PROJECT = "project"

    SCENE = "scene"

    MATERIAL = "material"

    ASSET = "asset"

    PIPELINE = "pipeline"

    WORKFLOW = "workflow"

    OTHER = "other"


class TemplateStatus(str, Enum):

    ACTIVE = "active"

    ARCHIVED = "archived"

    DISABLED = "disabled"


@dataclass(slots=True)
class TemplateMetadata:

    template_id: str

    name: str

    template_type: TemplateType

    created_at: str

    updated_at: str

    status: TemplateStatus

    version: int

    description: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    variables: dict[str, Any] = field(
        default_factory=dict
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class TemplateRecord:

    metadata: TemplateMetadata

    content: dict[str, Any] = field(
        default_factory=dict
    )


class TemplateManagerError(Exception):
    pass


class TemplateNotFound(
    TemplateManagerError
):
    pass


class TemplateRegistry:

    """
    Enterprise Thread Safe Template Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._templates: dict[
            str,
            TemplateRecord,
        ] = {}

    def add(
        self,
        template: TemplateRecord,
    ) -> None:

        with self._lock:

            self._templates[
                template.metadata.template_id
            ] = template

    def get(
        self,
        template_id: str,
    ) -> TemplateRecord:

        with self._lock:

            try:

                return self._templates[
                    template_id
                ]

            except KeyError as exc:

                raise TemplateNotFound(
                    template_id
                ) from exc

    def all(
        self,
    ) -> list[TemplateRecord]:

        with self._lock:

            return list(
                self._templates.values()
            )

    def remove(
        self,
        template_id: str,
    ) -> None:

        with self._lock:

            self._templates.pop(
                template_id
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._templates.clear()


class TemplateManager:

    """
    StudioOS Enterprise Template Manager

    Features:

    - Template Lifecycle Management
    - Project/Scene Templates
    - Variable Injection
    - Version Tracking
    - Event Integration
    - Shared State Integration
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    TEMPLATE_FILE = "templates.json"

    def __init__(
        self,
        workspace: SupportsWorkspace,
        *,
        event_bus: SupportsEventBus | None = None,
        shared_state: SupportsSharedState | None = None,
        runtime: SupportsRuntime | None = None,
        plugins: SupportsPluginManager | None = None,
    ) -> None:

        self._workspace = workspace

        self._event_bus = event_bus

        self._shared_state = shared_state

        self._runtime = runtime

        self._plugins = plugins

        self._lock = threading.RLock()

        self._registry = TemplateRegistry()

        self._root = (
            self._workspace.root /
            "templates"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.TEMPLATE_FILE
        )

        self._load()

# ============================================================
# File: studio/template_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _id() -> str:

        return uuid.uuid4().hex

    def _emit(
        self,
        event: str,
        **payload: Any,
    ) -> None:

        if self._event_bus is not None:

            self._event_bus.publish(
                event,
                **payload,
            )

        if self._plugins is not None:

            self._plugins.emit(
                event,
                **payload,
            )

    def _load(
        self,
    ) -> None:

        if not self._file.exists():

            return

        try:

            payload = json.loads(
                self._file.read_text(
                    encoding="utf-8",
                )
            )

            for item in payload:

                metadata = item[
                    "metadata"
                ]

                template = TemplateRecord(
                    metadata=TemplateMetadata(
                        template_id=metadata[
                            "template_id"
                        ],
                        name=metadata[
                            "name"
                        ],
                        template_type=TemplateType(
                            metadata[
                                "template_type"
                            ]
                        ),
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        status=TemplateStatus(
                            metadata[
                                "status"
                            ]
                        ),
                        version=metadata.get(
                            "version",
                            1,
                        ),
                        description=metadata.get(
                            "description",
                            "",
                        ),
                        tags=list(
                            metadata.get(
                                "tags",
                                [],
                            )
                        ),
                        variables=dict(
                            metadata.get(
                                "variables",
                                {},
                            )
                        ),
                        properties=dict(
                            metadata.get(
                                "properties",
                                {},
                            )
                        ),
                    ),
                    content=dict(
                        item.get(
                            "content",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    template
                )

        except Exception:

            return

    def _save(
        self,
    ) -> None:

        payload = [
            {
                "metadata":
                    asdict(
                        template.metadata
                    ),
                "content":
                    template.content,
            }
            for template
            in self._registry.all()
        ]

        self._file.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create(
        self,
        *,
        name: str,
        template_type: TemplateType,
        content: Mapping[
            str,
            Any,
        ],
        description: str = "",
        tags: list[str] | None = None,
        variables: Mapping[
            str,
            Any,
        ] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> TemplateRecord:

        with self._lock:

            template = TemplateRecord(
                metadata=TemplateMetadata(
                    template_id=self._id(),
                    name=name,
                    template_type=template_type,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=(
                        TemplateStatus.ACTIVE
                    ),
                    version=1,
                    description=description,
                    tags=list(
                        tags or []
                    ),
                    variables=dict(
                        variables or {}
                    ),
                    properties=dict(
                        properties or {}
                    ),
                ),
                content=dict(
                    content
                ),
            )

            self._registry.add(
                template
            )

            self._save()

            self._emit(
                "template.created",
                template_id=(
                    template.metadata.template_id
                ),
            )

            return template
        
# ============================================================
# File: studio/template_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get(
        self,
        template_id: str,
    ) -> TemplateRecord:

        return self._registry.get(
            template_id
        )

    def list_templates(
        self,
    ) -> list[TemplateRecord]:

        return self._registry.all()

    def update(
        self,
        template_id: str,
        *,
        content: Mapping[
            str,
            Any,
        ] | None = None,
        variables: Mapping[
            str,
            Any,
        ] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> TemplateRecord:

        with self._lock:

            template = self._registry.get(
                template_id
            )

            if content is not None:

                template.content = dict(
                    content
                )

            if variables is not None:

                template.metadata.variables.update(
                    variables
                )

            if properties is not None:

                template.metadata.properties.update(
                    properties
                )

            template.metadata.version += 1

            template.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "template.updated",
                template_id=template_id,
                version=(
                    template.metadata.version
                ),
            )

            return template

    def clone(
        self,
        template_id: str,
        new_name: str,
    ) -> TemplateRecord:

        with self._lock:

            source = self._registry.get(
                template_id
            )

            cloned = TemplateRecord(
                metadata=TemplateMetadata(
                    template_id=self._id(),
                    name=new_name,
                    template_type=(
                        source.metadata.template_type
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=(
                        TemplateStatus.ACTIVE
                    ),
                    version=1,
                    description=(
                        source.metadata.description
                    ),
                    tags=list(
                        source.metadata.tags
                    ),
                    variables=dict(
                        source.metadata.variables
                    ),
                    properties=dict(
                        source.metadata.properties
                    ),
                ),
                content=dict(
                    source.content
                ),
            )

            self._registry.add(
                cloned
            )

            self._save()

            self._emit(
                "template.cloned",
                source=template_id,
                template_id=(
                    cloned.metadata.template_id
                ),
            )

            return cloned

    def archive(
        self,
        template_id: str,
    ) -> TemplateRecord:

        with self._lock:

            template = self._registry.get(
                template_id
            )

            template.metadata.status = (
                TemplateStatus.ARCHIVED
            )

            template.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "template.archived",
                template_id=template_id,
            )

            return template

    def activate(
        self,
        template_id: str,
    ) -> TemplateRecord:

        with self._lock:

            template = self._registry.get(
                template_id
            )

            template.metadata.status = (
                TemplateStatus.ACTIVE
            )

            template.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "template.activated",
                template_id=template_id,
            )

            return template
        
# ============================================================
# File: studio/template_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def delete(
        self,
        template_id: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                template_id
            )

            self._save()

            self._emit(
                "template.deleted",
                template_id=template_id,
            )

    def find_by_type(
        self,
        template_type: TemplateType,
    ) -> list[TemplateRecord]:

        return [
            template
            for template
            in self._registry.all()
            if (
                template.metadata.template_type
                is template_type
            )
        ]

    def find_by_tag(
        self,
        tag: str,
    ) -> list[TemplateRecord]:

        return [
            template
            for template
            in self._registry.all()
            if tag
            in template.metadata.tags
        ]

    def render(
        self,
        template_id: str,
        variables: Mapping[
            str,
            Any,
        ],
    ) -> dict[str, Any]:

        with self._lock:

            template = self._registry.get(
                template_id
            )

            context = dict(
                template.metadata.variables
            )

            context.update(
                variables
            )

            return self._inject(
                template.content,
                context,
            )

    def _inject(
        self,
        value: Any,
        variables: Mapping[
            str,
            Any,
        ],
    ) -> Any:

        if isinstance(
            value,
            dict,
        ):

            return {
                key:
                    self._inject(
                        item,
                        variables,
                    )
                for key, item
                in value.items()
            }

        if isinstance(
            value,
            list,
        ):

            return [
                self._inject(
                    item,
                    variables,
                )
                for item
                in value
            ]

        if isinstance(
            value,
            str,
        ):

            result = value

            for key, item in variables.items():

                result = result.replace(
                    f"{{{{{key}}}}}",
                    str(item),
                )

            return result

        return value

    def export_template(
        self,
        template_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            template = self._registry.get(
                template_id
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    {
                        "metadata":
                            asdict(
                                template.metadata
                            ),
                        "content":
                            template.content,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_template(
        self,
        source: Path,
    ) -> TemplateRecord:

        with self._lock:

            if not source.exists():

                raise FileNotFoundError(
                    source
                )

            payload = json.loads(
                source.read_text(
                    encoding="utf-8",
                )
            )

            metadata = payload[
                "metadata"
            ]

            template = TemplateRecord(
                metadata=TemplateMetadata(
                    template_id=self._id(),
                    name=metadata[
                        "name"
                    ],
                    template_type=TemplateType(
                        metadata[
                            "template_type"
                        ]
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=TemplateStatus.ACTIVE,
                    version=1,
                    description=metadata.get(
                        "description",
                        "",
                    ),
                    tags=list(
                        metadata.get(
                            "tags",
                            [],
                        )
                    ),
                    variables=dict(
                        metadata.get(
                            "variables",
                            {},
                        )
                    ),
                    properties=dict(
                        metadata.get(
                            "properties",
                            {},
                        )
                    ),
                ),
                content=dict(
                    payload.get(
                        "content",
                        {},
                    )
                ),
            )

            self._registry.add(
                template
            )

            self._save()

            self._emit(
                "template.imported",
                template_id=(
                    template.metadata.template_id
                ),
            )

            return template
        
# ============================================================
# File: studio/template_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            templates = (
                self._registry.all()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.template_count",
                    len(templates),
                )

            self._emit(
                "template_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        templates = (
            self._registry.all()
        )

        types: dict[
            str,
            int,
        ] = {}

        statuses: dict[
            str,
            int,
        ] = {}

        for template in templates:

            template_type = (
                template.metadata.template_type.value
            )

            status = (
                template.metadata.status.value
            )

            types[template_type] = (
                types.get(
                    template_type,
                    0,
                )
                + 1
            )

            statuses[status] = (
                statuses.get(
                    status,
                    0,
                )
                + 1
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "template_count":
                len(templates),
            "types":
                types,
            "statuses":
                statuses,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "shared_state_connected":
                self._shared_state is not None,
            "plugin_manager_connected":
                self._plugins is not None,
        }

    def health_check(
        self,
    ) -> dict[str, Any]:

        invalid = []

        for template in (
            self._registry.all()
        ):

            if not template.metadata.name:

                invalid.append(
                    template.metadata.template_id
                )

        return {
            "healthy":
                not invalid,
            "invalid_templates":
                invalid,
            "registered_templates":
                len(
                    self._registry.all()
                ),
        }

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._registry.clear()

            self._save()

            self._emit(
                "template.registry.cleared",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "template_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()

