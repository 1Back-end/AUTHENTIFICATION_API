from datetime import datetime, date
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict,Json

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


class Storage(BaseModel):
    uuid: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None
    mimetype: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size: Optional[int] = None
    thumbnail: Any
    medium: Any
    date_added: Optional[datetime] = None
    date_modified: Optional[datetime] = None


class UserProfileResponse(BaseModel):
    user: User
    avatar: Optional[Storage]



class UserDetail(User):
    uuid: str
    avatar: Optional[Storage] = None



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
