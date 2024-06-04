from fastapi import APIRouter, Body, HTTPException
from typing import Any
from app.main.core.security import decode_access_token
from app.main.crud import user
from app.main.models import BlacklistToken
from app.main.models.db.session import SessionLocal

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.get("/validate-token/{token}", status_code=200)
async def validate_token(
        token: str,
):
    """Validate token"""
    db = SessionLocal()
    print(f".............token: {token}")
    if BlacklistToken.check_blacklist(db=db, auth_token=token):
        db.close()
        return False
    db.close()
    token = decode_access_token(token)
    print(f".............token: {token}")
    return token


@router.get("/get_user/{token}/{user_uuid}", status_code=200)
async def validate_token(
        token: str,
        user_uuid: str,
):
    """Validate token"""
    db = SessionLocal()
    if BlacklistToken.check_blacklist(db=db, auth_token=token):
        db.close()
        return False
    db.close()
    seller = user.get_by_uuid(db=db, uuid=user_uuid)
    if not seller:
        raise HTTPException(status_code=404, detail="User not found")
    return seller
