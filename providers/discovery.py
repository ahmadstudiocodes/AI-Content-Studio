"""
Arman StudioOS
Provider Discovery System

Automatic provider detection and registration.
"""

from __future__ import annotations

import importlib
import inspect

from pathlib import Path
from typing import List, Type

from .base import BaseProvider
from .registry import provider_registry



def discover_providers() -> List[str]:
    """
    Discover and register providers automatically.
    """

    registered = []

    base_path = Path(__file__).parent


    for folder in base_path.iterdir():

        if not folder.is_dir():
            continue


        if folder.name.startswith("_"):
            continue


        client_file = (
            folder / "client.py"
        )


        if not client_file.exists():
            continue


        module_name = (
            f"providers.{folder.name}.client"
        )


        try:

            module = importlib.import_module(
                module_name
            )


            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    issubclass(
                        obj,
                        BaseProvider
                    )
                    and obj is not BaseProvider
                ):

                    provider_id = (
                        folder.name.lower()
                    )


                    provider_registry.register(
                        obj,
                        provider_id,
                    )


                    registered.append(
                        provider_id
                    )


        except Exception as exc:

            print(
                f"Provider discovery failed: {module_name}",
                exc,
            )


    return registered



__all__ = [
    "discover_providers",
]