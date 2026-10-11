"""Read-only evidence checks for the bounded precision design candidate."""
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = '3e585f0e664bb222097a08dfe21d7c3298936d55'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

class Contract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.controls = []
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('form', 'input', 'select', 'textarea', 'option', 'button'):
            self.controls.append((tag, sorted(attrs.items())))
        if tag in ('script', 'link'):
            self.references.append((tag, sorted(attrs.items())))

old = Contract()
old.feed(git('show', BASE + ':app/static/index.html'))
new = Contract()
new.feed((ROOT / 'app/static/index.html').read_text(encoding='utf-8'))
assert Counter(old.ids) == Counter(new.ids)
assert len(new.ids) == len(set(new.ids))
assert old.controls == new.controls
assert old.references == new.references
changed_app = git('diff', BASE, '--name-only', '--', 'app').splitlines()
assert set(changed_app) == {'app/static/index.html', 'app/static/styles.css'}
source_hashes = {}
for name in git('ls-tree', '-r', '--name-only', BASE, 'app').splitlines():
    if name in changed_app:
        continue
    before = git('rev-parse', BASE + ':' + name)
    after = git('hash-object', '--path=' + name, name)
    assert before == after, name
    source_hashes[name] = after

# Only the newly created QA database is read; production/demo DBs are not opened.
sys.path.insert(0, str(ROOT))
from app.services.audit import digest
qa = Path((ROOT / 'data/precision-preview-location.txt').read_text(encoding='utf-8'))
assert qa.parent == ROOT / 'data' and qa.name.startswith('precision-preview-')
conn = sqlite3.connect('file:' + (qa / 'isolated.sqlite3').as_posix() + '?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
frozen = []
for name in ('ui-approved-export.json', 'ui-override-export.json'):
    record = json.loads((ROOT / 'evidence/release' / name).read_text(encoding='utf-8'))
    row = conn.execute('SELECT * FROM decisions WHERE id=?', (record['decision']['decision_id'],)).fetchone()
    # Discover the schema's ID/JSON names without assuming column positions.
    assert row is not None
    strings = dict(row)
    bundle = next(json.loads(v) for v in strings.values() if isinstance(v, str) and v.startswith('{') and '"snapshot"' in v)
    replay = {'mode': 'REPLAY', 'bundle_hash': record['bundle_hash'], **bundle}
    assert replay == record and digest(bundle) == record['bundle_hash']
    frozen.append({'export': name, 'bundle_hash': record['bundle_hash'], 'exact_replay_match': True})
counts = {table: conn.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0]
          for table in ('runs', 'snapshots', 'decisions', 'outbox')}
conn.close()
result = {'base': BASE, 'changed_application_files': changed_app,
          'html_ids_unique_and_unchanged': len(new.ids), 'controls_and_enum_values_unchanged': True,
          'script_and_stylesheet_references_unchanged': True,
          'unchanged_application_git_blobs': source_hashes, 'frozen_records': frozen,
          'isolated_qa_counts': counts,
          'candidate_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in changed_app}}
print(json.dumps(result, indent=2))
