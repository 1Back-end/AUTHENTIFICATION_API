from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.main.schemas import DataList


class UserBase(BaseModel):

    country_code: str
    phone_number: str
    first_name: str
    last_name: str
    email: str
    address: str
    birthday: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    date_added: datetime
    date_modified: datetime

class UserProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[str] = None


class UserDetail(User):
    uuid: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserList(DataList):
    data: List[User] = []


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserAuthentication(BaseModel):
    user: User
    token: Optional[Token] = None
    model_config = ConfigDict(from_attributes=True)
