"""Read-only follow-up audit; no production database or provider access."""
from pathlib import Path
import hashlib
import json
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'evidence/design/integrity-audit.py').read_text(encoding='utf-8')
source = source.replace("closurecall-record (5).json", "closurecall-record (6).json")
source = source.replace("prototype-draft (1).eml", "prototype-draft (2).eml")
source = source.replace("b6148326-f880-4cbc-b084-de486ce9d7a7", "2433f82b-35ea-4ce2-829e-bcaaabe59daf")
source = source.replace("'approval_json_exact'", "'delayed_override_json_exact'")
source = source.replace("evidence/design/final-integrity-and-downloads.json", "evidence/usability/integrity-and-downloads.json")
exec(compile(source, str(ROOT / 'evidence/design/integrity-audit.py'), 'exec'))
assert proof['counts'] == {'runs': 10, 'decisions': 9, 'outbox': 9}
manifest = json.loads((ROOT / 'evidence/design/manifest.json').read_text(encoding='utf-8'))
for name, expected in manifest['sha256'].items():
    data = (ROOT / 'evidence/design' / name).read_bytes()
    assert expected in (hashlib.sha256(data).hexdigest(), hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()), name
proof['retained_artifacts']['initial_design'] = {'files': len(manifest['sha256']), 'unchanged': True}
proof['downloads']['historical_memo_bytes_exact_scope'] = 'Previously downloaded initial-design memo rechecked; no new memo browser download in this follow-up.'
proof['followup_decisions'] = []
for ident in ('52c1e440-d904-4330-88d0-38e84cf25292', '2433f82b-35ea-4ce2-829e-bcaaabe59daf'):
    record = store.replay(ident)
    assert record['snapshot']['assessment']['recommended_posture'] == 'normal'
    proof['followup_decisions'].append({'decision_id': ident, 'status': record['decision']['status'], 'posture': record['decision']['posture'], 'original_recommendation': 'normal', 'timing_at': record['decision']['timing_at'], 'counts': record['notifications']['counts']})
(ROOT / 'evidence/usability/integrity-and-downloads.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'followup_integrity': 'VERIFIED', 'counts': proof['counts'], 'initial_design_artifacts_unchanged': len(manifest['sha256'])}))
