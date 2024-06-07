import uuid
from datetime import datetime, timedelta
from typing import Union,Optional
from app.main.core.i18n import __
from requests import Session
from app.main.schemas.file import FileUpload
from app.main.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.main.models import User
from app.main.schemas.file import FileUpload
from app.main import schemas, models
from app.main.core.security import get_password_hash, verify_password, generate_code
from app.main import utils


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
        # code = generate_code(length=9)[0:5]
        code = "00000"
        utils.NexahUtils.send_sms(phonenumber=db_obj.phone_number, body="Le code de validation de votre "
                                                                        "compte Epura est le suivant :    " + str(code))
        db_obj.otp = code
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

    @classmethod
    def get_by_uuid(cls, db: Session, *, uuid: str) -> Union[models.User, None]:
        return db.query(models.User).filter(models.User.uuid == uuid).first()


    @classmethod
    def update_profile(cls, db: Session, user_uuid: str, first_name: Optional[str] = None, last_name: Optional[str] = None, email: Optional[str] = None,address: Optional[str] = None, phone_number: Optional[str] = None,birthday: Optional[str] = None, avatar_file: Optional[FileUpload] = None):
        user = db.query(User).filter(User.uuid == user_uuid).first()
        
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.email = email if email else user.email
        user.address =  address if address else user.address
        user.phone_number = phone_number if phone_number else user.phone_number
        user.birthday = birthday if birthday else user.birthday
        user.full_phone_number=user.country_code + phone_number if phone_number else user.phone_number
        if avatar_file:
            file_url = cls.handle_file_upload(avatar_file)
            user.avatar.url = file_url
        
        db.commit()
        db.refresh(user)
        return user
        
    @staticmethod
    def handle_file_upload(file: FileUpload) -> str:
    
        pass

        

user = CRUDUser(models.User)
