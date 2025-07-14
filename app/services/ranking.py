from app.schemas.models import SenhaORM, UserORM
from app.utils.config import SessionLocal
from sqlalchemy import func

def obter_ranking_global():
   
    db = SessionLocal()
    try:
        # Subquery para obter o melhor tempo de cada usuário
        subquery = db.query(
            SenhaORM.user_id,
            func.min(SenhaORM.tempo_completado).label('melhor_tempo')
        ).group_by(SenhaORM.user_id).subquery()
        
        # Query principal para obter os dados completos
        ranking = db.query(
            UserORM.nome,
            UserORM.email,
            subquery.c.melhor_tempo,
            func.count(SenhaORM.id).label('total_senhas')
        ).join(
            subquery, UserORM.id == subquery.c.user_id
        ).join(
            SenhaORM, UserORM.id == SenhaORM.user_id
        ).group_by(
            UserORM.nome, UserORM.email, subquery.c.melhor_tempo
        ).order_by(
            subquery.c.melhor_tempo
        ).limit(10).all()  # Top 10
        
        return [
            {
                "posicao": idx + 1,
                "nome": item.nome,
                "email": item.email,
                "melhor_tempo": item.melhor_tempo,
                "total_senhas": item.total_senhas
            }
            for idx, item in enumerate(ranking)
        ]
    finally:
        db.close()

def obter_estatisticas_globais():
    db = SessionLocal()
    try:
        total_senhas = db.query(SenhaORM).count()
        if total_senhas == 0:
            return {"total_senhas": 0, "tempo_medio": 0, "melhor_tempo_global": 0}
        
        soma_tempos = db.query(SenhaORM).with_entities(
            func.sum(SenhaORM.tempo_completado)
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