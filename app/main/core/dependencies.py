from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, BackgroundTasks

from app.main import schemas
from app.main.core.i18n import __
from app.main.core.security import decode_access_token


def get_db(request: Request) -> Generator:
    return request.state.db


class TokenRequired(HTTPBearer):

    def __init__(self, auto_error: bool = False):
        super(TokenRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

        credentials: HTTPAuthorizationCredentials = await super(TokenRequired, self).__call__(request)
        credentials_exception = HTTPException(status_code=401, detail=__('invalid-credentials'),
                                              headers={"WWW-Authenticate": "Bearer"})
        if credentials:
            if not credentials.scheme == "Bearer":
                raise credentials_exception

            data = None
            token_data = decode_access_token(credentials.credentials)
            if not token_data:
                raise credentials_exception

            current_user = schemas.User(
                user_id=token_data['user_id'],
                user_email=token_data['sub'],
            )

            return current_user

        else:
            raise HTTPException(status_code=401, detail=__('invalid-credentials'))

