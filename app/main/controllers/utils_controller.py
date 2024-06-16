from fastapi import APIRouter, HTTPException

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
    current_user = user.get_by_uuid(db=db, uuid=user_uuid)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@router.get("/get_users/{token}/{uuid}", status_code=200)
async def get_users(
        token: str,
        uuid: str,
):
    """Get users"""
    db = SessionLocal()
    if BlacklistToken.check_blacklist(db=db, auth_token=token):
        db.close()
        return False
    db.close()
    print(f"...........uuid come from front:{uuid}")
    print(".............new format_buyer:{}, seller:{}".format(decode_access_token(token)['sub'], uuid))
    users = []
    user1 = user.get_by_uuid(db=db, uuid=decode_access_token(token)['sub'])
    user2 = user.get_by_uuid(db=db, uuid=uuid)
    if not user1:
        raise HTTPException(status_code=404, detail="User not found")
    users.append(user1)
    if not user2:
        raise HTTPException(status_code=404, detail="User not found")
    users.append(user2)
    print(".............buyer:{}, seller:{}".format(user1, user2))
    return users
