
from app.main.crud.base import CRUDBase
from app.main.models.storage import Storage
from app.main.schemas.user import UserCreate, UserUpdate
from app.main.schemas.file import File
from sqlalchemy.orm import Session
from typing import Any
from app.main.utils.file import FileUtils


class CRUDFile(CRUDBase[File, UserCreate,UserUpdate]):
    @classmethod
    def store_file(cls, db: Session, base_64: Any, name: str = None) -> Storage:
        if "#" in name:
            name = name.replace("", "$§£")
        file_manager = FileUtils(base64=base_64, name=name)
        storage = file_manager.save(db=db)
        print(f".........................image store:{storage}")
        return storage


file_storage = CRUDFile(Storage)
