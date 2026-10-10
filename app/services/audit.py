import hashlib
import json
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

def timestamp():
    return utcnow().isoformat()

def parse_time(value):
    if value is None:
        return None
    date = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    return date.astimezone(timezone.utc)

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()
