from fastapi import Header, HTTPException
from backend.config import settings

async def verify_superadmin_token(x_superadmin_token: str = Header(None)):
    """
    Enforce SuperAdmin authorization via request header.
    Expects X-SuperAdmin-Token matching settings.superadmin_token.
    """
    expected = settings.superadmin_token or "lifodial2026"
    if not x_superadmin_token or x_superadmin_token != expected:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized admin access"
        )
