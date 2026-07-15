from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class DiagnosticsSnapshot:

    state: str

    components: Dict[str, Any]


class RuntimeDiagnostics:
    """
    Runtime diagnostic snapshot provider.
    """

    def snapshot(
        self,
        state: str,
        components: Dict[str, Any],
    ) -> DiagnosticsSnapshot:

        return DiagnosticsSnapshot(
            state=state,
            components=components,
        )

    def validate(
        self,
        snapshot: DiagnosticsSnapshot,
    ) -> Dict[str, Any]:

        report = {
            "healthy": True,
            "issues": [],
            "component_count": len(
                snapshot.components
            ),
        }

        if not snapshot.state:

            report["healthy"] = False

            report["issues"].append(
                "Missing runtime state."
            )

        for name, component in (
            snapshot.components.items()
        ):

            if component is None:

                report["healthy"] = False

                report["issues"].append(
                    f"Component '{name}' is unavailable."
                )

        return report


runtime_diagnostics = RuntimeDiagnostics()