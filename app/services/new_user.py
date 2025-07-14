from app.schemas.models import User, UserORM
from app.utils.config import SessionLocal
from sqlalchemy.exc import IntegrityError

def create_user(user: User):
    db = SessionLocal()
    db_user = UserORM(nome=user.nome, email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        user = db.query(UserORM).filter(UserORM.email == email).first()
        return user
    finally:
        db.close()