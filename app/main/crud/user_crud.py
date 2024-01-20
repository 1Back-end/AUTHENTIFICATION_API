import uuid
from datetime import datetime, timedelta
from typing import Union

from requests import Session

from app.main.crud.base import CRUDBase

from app.main import schemas, models
from app.main.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):

    @classmethod
    def authenticate(cls, db: Session, *, phone_number: str, password: str) -> Union[models.User, None]:
        db_obj: models.User = db.query(models.User).filter(models.User.full_phone_number == phone_number).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None
        return db_obj

    @classmethod
    def get_by_phone_number(cls, db: Session, *, phone_number: str) -> Union[models.User, None]:
        return db.query(models.User).filter(models.User.full_phone_number == phone_number).first()

    @classmethod
    def get_by_email(cls, db: Session, *, email: str) -> Union[models.User, None]:
        return db.query(models.User).filter(models.User.email == email).first()

    @classmethod
    def resend_otp(cls, db: Session, *, db_obj: models.User) -> models.User:
        db_obj.otp = "00000"
        db_obj.otp_expired_at = datetime.now() + timedelta(minutes=5)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            uuid=str(uuid.uuid4()),
            full_phone_number=f"{obj_in.country_code}{obj_in.phone_number}",
            country_code=obj_in.country_code,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            status=models.UserStatusType.UNACTIVED,
            birthday=obj_in.birthday if obj_in.birthday else None,
            address=obj_in.address if obj_in.address else None,
        )
        db.add(db_obj)
        db.commit()
        cls.resend_otp(db=db, db_obj=db_obj)
        return db_obj


user = CRUDUser(models.User)
