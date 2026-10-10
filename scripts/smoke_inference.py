import asyncio
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.settings import settings
from app.jobs import bounded_worker

async def main():
    if not settings.ai_available:
        print('BLOCKED: INFERENCE_API_KEY missing/placeholder or endpoint unapproved. No model request made.')
        return 2
    result=await bounded_worker('app.agent.smoke_worker',{})
    print(json.dumps(result))
    Path('data').mkdir(exist_ok=True)
    Path('data/inference-smoke.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['status']=='pass' else 1

if __name__=='__main__':
    sys.exit(asyncio.run(main()))
