from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env', override=False, encoding='utf-8-sig')

def configured(value: str) -> bool:
    return bool(value and not value.startswith('replace-'))

@dataclass(frozen=True)
class Settings:
    database: str = os.getenv('DATABASE_PATH', str(ROOT / 'data/closurecall.sqlite3'))
    environment: str = os.getenv('APP_ENV', 'development')
    timezone: str = os.getenv('APP_TIMEZONE', 'America/Chicago')
    nws_user_agent: str = os.getenv('NWS_USER_AGENT', 'ClosureCallHack/1.0 (local prototype)')
    inference_base_url: str = os.getenv('INFERENCE_BASE_URL', 'https://ws.akamai-workshops.com/v1')
    inference_model: str = os.getenv('INFERENCE_MODEL', 'hackathon-chat')
    inference_key: str = os.getenv('INFERENCE_API_KEY', '')
    manager_username: str = os.getenv('MANAGER_USERNAME', 'manager')
    manager_password: str = os.getenv('MANAGER_PASSWORD', '')
    http_timeout: float = float(os.getenv('HTTP_TIMEOUT_SECONDS', '15'))
    nws_freshness: int = int(os.getenv('NWS_FETCH_FRESHNESS_SECONDS', '600'))
    aq_max_age: int = int(os.getenv('AQ_VALID_TIME_MAX_AGE_SECONDS', '10800'))
    agent_deadline: int = int(os.getenv('AGENT_DEADLINE_SECONDS', '90'))
    agent_tool_limit: int = int(os.getenv('AGENT_MAX_TOOL_CALLS', '8'))
    agent_model_limit: int = int(os.getenv('AGENT_MAX_MODEL_CALLS', '6'))
    concurrency: int = int(os.getenv('MAX_CONCURRENT_EVALUATIONS', '1'))
    notification_mode: str = os.getenv('NOTIFICATION_MODE', 'outbox_only')
    deployment: str = os.getenv('DEPLOYMENT_LABEL', 'Local development')
    build: str = os.getenv('BUILD_COMMIT', 'no-commit-yet')

    def __post_init__(self):
        if self.timezone != 'America/Chicago':
            raise ValueError('Kansas City preset requires America/Chicago; explorer sites use verified timezones')
        if self.concurrency != 1 or self.notification_mode != 'outbox_only':
            raise ValueError('MVP requires one evaluation and outbox_only')
        if min(self.http_timeout, self.nws_freshness, self.aq_max_age, self.agent_deadline,
               self.agent_tool_limit, self.agent_model_limit) <= 0:
            raise ValueError('Budgets must be positive')

    @property
    def ai_available(self):
        # No unapproved provider switch from a local environment change.
        return (configured(self.inference_key) and
                self.inference_base_url.rstrip('/') == 'https://ws.akamai-workshops.com/v1')

settings = Settings()
