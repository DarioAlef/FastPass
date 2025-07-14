from app.schemas.models import Senha, SenhaORM
from app.utils.config import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

def salvar_senha(senha: Senha):
    db = SessionLocal()
    try:
        db_senha = SenhaORM(
            senha=senha.senha,
            tempo_completado=senha.tempo_completado,
            user_id=senha.user_id
        )
        db.add(db_senha)
        db.commit()
        db.refresh(db_senha)
        return db_senha
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def obter_senhas_usuario(user_id: int):
    db = SessionLocal()
    try:
        senhas = db.query(SenhaORM).filter(
            SenhaORM.user_id == user_id
        ).order_by(desc(SenhaORM.data_criacao)).all()
        return senhas
    finally:
        db.close()

def obter_melhor_tempo_usuario(user_id: int):
    db = SessionLocal()
    try:
        melhor_senha = db.query(SenhaORM).filter(
            SenhaORM.user_id == user_id
        ).order_by(SenhaORM.tempo_completado).first()
        return melhor_senha.tempo_completado if melhor_senha else None
    finally:
        db.close()