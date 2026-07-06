import shutil
from pathlib import Path
from datetime import datetime


def create_backup():

    source = Path("database/studio.db")

    if not source.exists():
        return

    Path("backups").mkdir(
        exist_ok=True
    )

    name = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    shutil.copy(
        source,
        f"backups/studio_{name}.db"
    )

    print("Backup Created.")