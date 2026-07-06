#!/usr/bin/env python3
"""
AI Content Studio - Project Generator
Version: 0.1.0
Author: Ahmad + Arman
"""

from pathlib import Path
from datetime import datetime
import json

VERSION = "0.1.0"

FOLDERS = [
    "core",
    "brain",
    "memory",
    "agents",
    "database",
    "dashboard",
    "channels",
    "platforms",
    "modules",
    "voice",
    "config",
    "docs",
    "logs",
    "backups",
    "tests",
    "assets",
    "scripts",
]

FILES = {
    "README.md": "# AI Content Studio\n",
    "requirements.txt": "",
    ".gitignore": "",
}


def create_structure(base: Path):

    print("\nCreating folders...\n")

    for folder in FOLDERS:
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] {folder}")

    print("\nCreating files...\n")

    for filename, content in FILES.items():
        file = base / filename

        if not file.exists():
            file.write_text(content, encoding="utf-8")
            print(f"[NEW] {filename}")
        else:
            print(f"[SKIP] {filename}")

    version = {
        "version": VERSION,
        "created": datetime.now().isoformat()
    }

    config = base / "config" / "version.json"

    config.write_text(
        json.dumps(version, indent=4),
        encoding="utf-8"
    )

    print("\nProject Generated Successfully.")


if __name__ == "__main__":

    BASE = Path.cwd()

    create_structure(BASE)