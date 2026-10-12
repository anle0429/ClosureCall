import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import Store
from app.settings import settings

if __name__ == "__main__":
    Store(settings.database).initialize()
    print(
        "Schema and synthetic facility seeded idempotently; existing history preserved."
    )
