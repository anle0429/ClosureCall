"""Scan staged/tracked source and authenticated API responses without printing secrets."""
import argparse
import re
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import httpx
from app.settings import settings, configured

def check(body, values):
    private_block=re.compile(rb'-----BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY-----\r?\n[A-Za-z0-9+/=\r\n]{64,}')
    return any(value.encode() in body for value in values) or private_block.search(body) is not None

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--decision-id')
    args=parser.parse_args()
    secrets=[value for value in (settings.manager_password,settings.inference_key) if configured(value)]
    paths=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
    failed=[]
    count=0
    for path in filter(None,paths):
        count+=1
        if path=='.env' or (path.startswith('.env.') and path!='.env.example') or check(Path(path).read_bytes(),secrets):
            failed.append(path)
    api_count=0
    if args.decision_id:
        routes=['/health','/api/config','/api/facilities',f'/api/decisions/{args.decision_id}',
                f'/api/decisions/{args.decision_id}/replay',f'/api/decisions/{args.decision_id}/notifications',
                f'/api/decisions/{args.decision_id}/export']
        with httpx.Client(base_url='http://127.0.0.1:8000',auth=(settings.manager_username,settings.manager_password)) as client:
            for route in routes:
                response=client.get(route)
                response.raise_for_status()
                api_count+=1
                if check(response.content,secrets):failed.append(route)
    if failed:
        print('FAIL: sensitive values found in these paths/routes only:',failed)
        sys.exit(1)
    print(f'PASS: {count} source files and {api_count} API responses contain no configured secrets/private keys.')
