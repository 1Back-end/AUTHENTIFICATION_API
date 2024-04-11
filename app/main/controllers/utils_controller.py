from fastapi import APIRouter, Body

from app.main.core.security import is_apikey
from app.main.models import BlacklistToken
from app.main.models.db.session import SessionLocal

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.get("/validate-token/{token}", response_model=bool, status_code=200)
async def validate_token(
        token: str,
        api_key: str = Body(...)
) -> bool:
    """Validate token"""
    is_apikey(api_key=api_key)
    db = SessionLocal()
    if BlacklistToken.check_blacklist(db=db, auth_token=token):
        db.close()
        return False
    db.close()
    return True
