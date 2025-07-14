from app.schemas.models import Senha, SenhaORM
from app.utils.config import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

def salvar_senha(senha: Senha):
    """Salva uma senha válida no banco de dados"""
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
    """Obtém todas as senhas de um usuário específico"""
    db = SessionLocal()
    try:
        senhas = db.query(SenhaORM).filter(
            SenhaORM.user_id == user_id
        ).order_by(desc(SenhaORM.data_criacao)).all()
        return senhas
    finally:
        db.close()

def obter_melhor_tempo_usuario(user_id: int):
    """Obtém o melhor tempo de um usuário específico"""
    db = SessionLocal()
    try:
        melhor_senha = db.query(SenhaORM).filter(
            SenhaORM.user_id == user_id
        ).order_by(SenhaORM.tempo_completado).first()
        return melhor_senha.tempo_completado if melhor_senha else None
    finally:
        db.close()

def obter_estatisticas_globais():
    """Obtém estatísticas globais do sistema"""
    db = SessionLocal()
    try:
        total_senhas = db.query(SenhaORM).count()
        if total_senhas == 0:
            return {"total_senhas": 0, "tempo_medio": 0, "melhor_tempo_global": 0}
        
        soma_tempos = db.query(SenhaORM).with_entities(
            db.func.sum(SenhaORM.tempo_completado)
        ).scalar()
        
        melhor_tempo = db.query(SenhaORM).order_by(
            SenhaORM.tempo_completado
        ).first()
        
        return {
            "total_senhas": total_senhas,
            "tempo_medio": soma_tempos / total_senhas,
            "melhor_tempo_global": melhor_tempo.tempo_completado if melhor_tempo else 0
        }
    finally:
        db.close()