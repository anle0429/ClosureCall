import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import Store
from app.settings import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("decision_id")
    args = parser.parse_args()
    bundle = Store(settings.database).replay(args.decision_id)
    destination = Path("data/exports") / (args.decision_id + ".json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise SystemExit("Destination exists; refusing overwrite")
    destination.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(destination)
