from fastapi import HTTPException, Header
from app.auth.security import decode_access_token

def get_current_user_email(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # SAFE token extraction (supports both formats)
    if authorization.lower().startswith("bearer "):
        parts = authorization.split(" ", 1)
        if len(parts) != 2 or not parts[1]:
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        token = parts[1]
    else:
        token = authorization

    try:
        email = decode_access_token(token)
        return email.strip().lower()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
