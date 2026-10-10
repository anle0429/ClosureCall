import asyncio
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.clients import nws, air_quality
from app.services.audit import timestamp

async def main():
    weather, aq = await asyncio.gather(nws.point(39.0997, -94.5786), air_quality.point(39.0997, -94.5786))
    result = {'mode': 'LIVE', 'tested_at': timestamp(), 'nws': weather, 'air_quality': aq}
    destination = Path('data/source-smoke.json')
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'nws_status': weather['status'], 'nws_http': weather['response_status'],
                      'alert_count': len(weather['alerts']), 'aq_status': aq['status'],
                      'aq_http': aq['response_status'], 'aq_valid_at': aq['valid_at_utc'],
                      'us_aqi': aq['us_aqi'], 'evidence_file': str(destination)}))
    return 0 if weather['status'] == aq['status'] == 'available' else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
