from pathlib import Path

FOLDERS = [
    "brain",
    "memory",
    "agents",
    "channels",
    "dashboard",
    "database",
    "docs",
    "config",
    "logs",
    "assets",
    "plugins",
    "voice",
    "api",
    "backups",
    "tests",
    "temp"
]


def create_project_structure():
    print("\nCreating Project Structure...\n")

    for folder in FOLDERS:
        Path(folder).mkdir(exist_ok=True)
        print(f"✔ {folder}")