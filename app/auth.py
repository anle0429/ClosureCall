import secrets
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.settings import settings, configured

security = HTTPBasic(auto_error=False)


def manager(
    request: Request, credentials: HTTPBasicCredentials | None = Depends(security)
):
    if not configured(settings.manager_password):
        raise HTTPException(
            503, "Configure MANAGER_PASSWORD locally; placeholders rejected"
        )
    valid_user = credentials is not None and secrets.compare_digest(
        credentials.username.encode(), settings.manager_username.encode()
    )
    valid_pass = credentials is not None and secrets.compare_digest(
        credentials.password.encode(), settings.manager_password.encode()
    )
    if not valid_user or not valid_pass:
        raise HTTPException(
            401,
            "Manager authentication required",
            headers={"WWW-Authenticate": 'Basic realm="ClosureCall"'},
        )
    # Same-origin frontend. Reject cross-origin browser mutations even with cached Basic auth.
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        origin = request.headers.get("origin")
        if origin and origin.rstrip("/") != str(request.base_url).rstrip("/"):
            raise HTTPException(403, "Cross-origin mutation rejected")
    return credentials.username
