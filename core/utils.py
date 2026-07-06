from pathlib import Path
from datetime import datetime


def ensure_folder(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )