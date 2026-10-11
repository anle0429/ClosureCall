"""Read-only integrity/download audit for the separate design QA database."""
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from app.db import Store
from app.services.memo import render_memo

folder = Path((ROOT / 'data/design-preview-location.txt').read_text().strip())
assert folder.resolve().is_relative_to((ROOT / 'data').resolve()) and folder.name.startswith('design-preview-')
store = Store(folder / 'isolated.sqlite3')
proof = {'scope': 'Isolated design QA only; not a production or live-provider test',
         'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'original_records': []}
for name in ('ui-approved-export.json', 'ui-override-export.json'):
    original = json.loads((ROOT / 'evidence/release' / name).read_text(encoding='utf-8'))
    current = store.replay(original['decision']['decision_id'])
    assert current == original
    proof['original_records'].append({'decision_id': original['decision']['decision_id'],
                                      'bundle_hash': current['bundle_hash'], 'exact_match': True})
with store.connection() as conn:
    proof['counts'] = {name: conn.execute(f'SELECT count(*) FROM {name}').fetchone()[0]
                       for name in ('runs', 'decisions', 'outbox')}
    proof['per_run_decisions'] = [dict(row) for row in conn.execute('SELECT run_id,count(*) AS decisions FROM decisions GROUP BY run_id')]
    assert all(row['decisions'] == 1 for row in proof['per_run_decisions'])
    assert proof['counts']['decisions'] == proof['counts']['outbox']
    proof['new_records'] = []
    original_ids = {row['decision_id'] for row in proof['original_records']}
    for row in conn.execute('SELECT id FROM decisions ORDER BY rowid'):
        if row['id'] in original_ids:
            continue
        record = store.replay(row['id'])
        assert record['snapshot']['test_evidence_label'].startswith('SYNTHETIC')
        assert record['metrics']['model_calls'] == record['metrics']['source_http_attempts'] == 0
        proof['new_records'].append({'decision_id': row['id'], 'run_id': record['decision']['evaluation_id'],
                                     'status': record['decision']['status'], 'posture': record['decision']['posture'],
                                     'counts': record['notifications']['counts'], 'source_http_attempts': 0, 'model_calls': 0})
downloads = Path.home() / 'Downloads'
export = json.loads((downloads / 'closurecall-record (5).json').read_text(encoding='utf-8'))
assert export == store.replay(export['decision']['decision_id'])
eml = BytesParser(policy=policy.default).parsebytes((downloads / 'prototype-draft (1).eml').read_bytes())
record = store.replay('b6148326-f880-4cbc-b084-de486ce9d7a7')
person = next(p for p in record['notifications']['recipients'] if p['employee_id'] == 'demo-08')
assert str(eml['To']) == person['email'] and str(eml['Subject']) == person['subject']
assert eml.get_content().replace('\r\n', '\n').rstrip('\n') == person['message'].rstrip('\n')
memo = (downloads / 'closurecall-decision-memo (2).html').read_bytes()
assert memo == render_memo(store.replay('16a170c1-af9b-4950-86b2-a3eecf1ad26b')).encode('utf-8')
proof['downloads'] = {'approval_json_exact': True, 'essential_eml_headers_and_content_exact': True,
                      'historical_memo_bytes_exact': True, 'memo_visual_print': 'NOT VERIFIED'}
retained = {}
for rel in ('evidence/release', 'evidence/release-followup', 'evidence/feedback'):
    manifest = json.loads((ROOT / rel / 'manifest.json').read_text(encoding='utf-8'))
    files = manifest.get('file_sha256', manifest.get('sha256'))
    for name, expected in files.items():
        path = ROOT / rel / name
        if not path.exists():
            path = ROOT / name
        data = path.read_bytes()
        assert expected in (hashlib.sha256(data).hexdigest(), hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()), name
    retained[rel] = {'files': len(files), 'unchanged': True}
package = json.loads((ROOT / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
for name, value in package['files'].items():
    data = (ROOT / name).read_bytes()
    assert len(data) == value['bytes'] and hashlib.sha256(data).hexdigest() == value['sha256']
retained['user_package'] = {'files': len(package['files']), 'unchanged': True}
proof['retained_artifacts'] = retained
changed = subprocess.check_output(['git', 'diff', '--name-only', 'c3d9c5673847c62a2ee824c6bf52230fc0f628d7', '--', 'app', 'tests', 'requirements.txt', 'requirements-linux.lock', 'Dockerfile', 'compose.yaml'], cwd=ROOT, text=True).splitlines()
assert set(changed) == {'app/static/app.js', 'app/static/index.html', 'app/static/styles.css'}
proof['application_diff'] = changed
(ROOT / 'evidence/design/final-integrity-and-downloads.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'integrity_audit': 'VERIFIED', 'counts': proof['counts'], 'downloads': proof['downloads'], 'retained': retained}))
