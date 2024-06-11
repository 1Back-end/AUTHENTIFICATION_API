import json
import os
import shutil
import platform
from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Column, String
from app.main import schemas
from app.main.core.config import Config
from app.main.core import dependencies
from app.main.models.db.base_class import Base
from app.main.utils import logger
from app.main import models,crud

router = APIRouter(prefix="/migrations", tags=["migrations"])


def check_user_access_key(admin_key: schemas.AdminKey):
    logger.info(f"Check user access key: {admin_key.key}")
    if admin_key.key not in [Config.ADMIN_KEY]:
        raise HTTPException(status_code=400, detail="Clé d'accès incorrecte")


@router.post("/create-database-tables", response_model=schemas.Msg, status_code=201)
async def create_database_tables(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create database structure (tables)
    """
    check_user_access_key(admin_key)
    """ Try to remove previous alembic tags in database """
    try:
        @dataclass
        class AlembicVersion(Base):
            __tablename__ = "alembic_version"
            version_num: str = Column(String(32), primary_key=True, unique=True)

        db.query(AlembicVersion).first().delete()
        db.commit()
    except Exception as e:
        pass

    """ Try to remove previous alembic versions folder """
    migrations_folder = os.path.join(os.getcwd(), "alembic", "versions")
    try:
        shutil.rmtree(migrations_folder)
    except Exception as e:
        pass

    """ create alembic versions folder content """
    try:
        os.mkdir(migrations_folder)
    except OSError:
        logger.error("Creation of the directory %s failed" % migrations_folder)
    else:
        logger.error("Successfully created the directory %s " % migrations_folder)

    try:
        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\.venv\Scripts\python.exe -m alembic revision --autogenerate')

        else:
            os.system('PYTHONPATH=. alembic revision --autogenerate')

        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\.venv\Scripts\python.exe -m alembic upgrade head')

        else:
            os.system('PYTHONPATH=. alembic upgrade head')

        """ Try to remove previous alembic versions folder """
        try:
            shutil.rmtree(migrations_folder)
            pass
        except Exception as e:
            pass

        return {"message": "Les tables de base de données ont été créées avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-users", response_model=schemas.Msg, status_code=201)
def create_users(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default users
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/users.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                user= db.query(models.User).filter(models.User.uuid == data["uuid"]).first()
                if not user:
                    user = models.User(
                        uuid = data["uuid"],
                        country_code = data["country_code"],
                        phone_number = data["phone_number"],
                        full_phone_number = data["full_phone_number"],
                        first_name = data["first_name"],
                        last_name = data["last_name"],
                        email = data["email"],
                        address = data["address"],
                        birthday = data["birthday"],
                        otp = data["otp"],
                        otp_expired_at = data["otp_expired_at"],
                        otp_password = data["otp_password"],
                        otp_password_expired_at = data ["otp_password_expired_at"],
                        password_hash= data["password_hash"],
                        status = data["status"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"]
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)
        return {"message": "users  created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")
