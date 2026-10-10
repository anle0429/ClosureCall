import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import httpx
from app.settings import settings
from app.services.audit import digest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Read-only historical replay integrity check before/after service restart')
    parser.add_argument('decision_id')
    parser.add_argument('--url',default='http://127.0.0.1:8000')
    args=parser.parse_args()
    if args.url not in ('http://127.0.0.1:8000','http://127.0.0.1:8080','http://127.0.0.1:8081'):
        raise SystemExit('Only local/SSH-tunnel URL allowed')
    with httpx.Client(base_url=args.url,auth=(settings.manager_username,settings.manager_password)) as client:
        response=client.get(f'/api/decisions/{args.decision_id}/replay')
        response.raise_for_status()
        body=response.json()
    bundle={k:v for k,v in body.items() if k not in ('mode','bundle_hash')}
    assert digest(bundle)==body['bundle_hash']
    baseline=Path('data/replay-baseline-'+args.decision_id+'.json')
    if baseline.exists():
        assert json.loads(baseline.read_text(encoding='utf-8'))==body
        print('PASS: historical bundle and drafts exactly match baseline after restart/read')
    else:
        baseline.write_text(json.dumps(body,indent=2),encoding='utf-8')
        print('PASS: historical bundle integrity verified; baseline saved for restart comparison')
    print(json.dumps({'decision_id':args.decision_id,'bundle_hash':body['bundle_hash'],
                      'counts':body['notifications']['counts'],'ai_status':body['ai']['status']}))
