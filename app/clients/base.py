import asyncio
import hashlib
import httpx
from app.services.audit import timestamp
from app.settings import settings

async def fetch_json(url, params=None, nws=False):
    headers = {'Accept': 'application/geo+json' if nws else 'application/json'}
    if nws:
        agent = settings.nws_user_agent
        headers['User-Agent'] = agent if 'replace-' not in agent else 'ClosureCallHack/1.0 (local hackathon prototype)'
    async with httpx.AsyncClient(timeout=settings.http_timeout, follow_redirects=False) as client:
        request = client.build_request('GET', url, params=params, headers=headers)
        meta = {'source_url': str(request.url), 'fetched_at_utc': timestamp(),
                'request_started_at_utc': timestamp(), 'http_attempts':0,
                'response_status': None, 'raw_response_sha256': None, 'status': 'unavailable'}
        try:
            # Entire retry sequence has one total wall-clock budget.
            async with asyncio.timeout(settings.http_timeout):
                for attempt in range(2):
                    meta['http_attempts']+=1
                    try:
                        response = await client.send(request)
                    except httpx.TransportError:
                        if attempt == 0:
                            await asyncio.sleep(.5)
                            continue
                        raise
                    meta['response_status'] = response.status_code
                    meta['fetched_at_utc'] = timestamp()
                    meta['raw_response_sha256'] = hashlib.sha256(response.content).hexdigest()
                    if response.status_code in (429, 500, 502, 503, 504) and attempt == 0:
                        retry = response.headers.get('Retry-After', '0.5')
                        try:
                            delay = float(retry)
                        except ValueError:
                            delay = settings.http_timeout  # do not ignore an unparsed rate limit
                        if delay >= settings.http_timeout or delay < 0:
                            break
                        await asyncio.sleep(delay)
                        continue
                    break
                response.raise_for_status()
                body = response.json()
                if not isinstance(body, dict):
                    raise ValueError('Expected JSON object')
                meta['status'] = 'available'
                return body, meta
        except (httpx.HTTPError, TimeoutError, ValueError) as exc:
            meta['safe_error_code'] = type(exc).__name__
        return None, meta
