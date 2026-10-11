"""Check staged content; report only paths and aggregate results, never values."""
import json
from pathlib import Path
import re
import subprocess
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
files = subprocess.check_output(['git', 'diff', 'c3d9c5673847c62a2ee824c6bf52230fc0f628d7', '--name-only', '--diff-filter=ACM'], cwd=ROOT, text=True).splitlines()
config = dotenv_values(ROOT / '.env')
secrets = [str(config[k]).encode() for k in ('MANAGER_PASSWORD', 'INFERENCE_API_KEY') if config.get(k) and len(str(config[k])) >= 8]
patterns = [rb'-----BEGIN (?:OPENSSH|RSA|EC|DSA|ENCRYPTED) PRIVATE KEY-----',
            rb'hk__[A-Za-z0-9_-]{20,}', rb'gh[pousr]_[A-Za-z0-9]{20,}',
            rb'Authorization:\s*(?:Basic|Bearer)\s+[A-Za-z0-9+/=_-]{15,}']
findings = []
for name in files:
    if name == '.env' or name.startswith(('data/', 'backups/')) or name.endswith(('.sqlite3', '.pem', '.key')):
        findings.append({'file': name, 'reason': 'forbidden runtime path'})
        continue
    data = subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT)
    if any(secret in data for secret in secrets) or any(re.search(pattern, data) for pattern in patterns):
        findings.append({'file': name, 'reason': 'secret pattern'})
result = {'scope': 'Candidate source plus staged design changes against c3d9c56; configured manager/inference values compared in memory; no secret output',
          'files_scanned': len(files), 'configured_values_checked': len(secrets), 'findings': findings}
print(json.dumps(result))
if findings:
    raise SystemExit(1)
