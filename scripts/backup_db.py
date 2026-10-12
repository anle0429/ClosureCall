import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.settings import settings
from app.services.audit import utcnow


def backup(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise ValueError("Backup destination exists; refusing overwrite")
    # Read-only source prevents silently creating an empty missing database.
    with sqlite3.connect(Path(source).resolve().as_uri() + "?mode=ro", uri=True) as src:
        with sqlite3.connect(destination) as target:
            src.backup(target)


if __name__ == "__main__":
    name = (
        Path(settings.database).resolve().parent
        / "backups"
        / ("closurecall-" + utcnow().strftime("%Y%m%dT%H%M%SZ") + ".sqlite3")
    )
    backup(settings.database, name)
    print("SQLite backup created:", name)
