from fastapi import status, APIRouter, HTTPException
from app.schemas.models import Senha, SenhaResponse
from app.services.password_manager import (
    salvar_senha, 
    obter_senhas_usuario, 
    obter_melhor_tempo_usuario
)
from app.services.ranking import (
    obter_estatisticas_globais,
    obter_ranking_global
)
from typing import List

router = APIRouter()

@router.post("/senha/salvar", status_code=status.HTTP_201_CREATED)
async def salvar_senha_valida(senha: Senha):
    """Salva uma senha que passou em todos os critérios"""
    db_senha = salvar_senha(senha)
    if db_senha:
        return {
            "msg": "Senha salva com sucesso!",
            "id": db_senha.id,
            "tempo_completado": db_senha.tempo_completado
        }
    raise HTTPException(status_code=400, detail="Erro ao salvar senha")

@router.get("/senha/usuario/{user_id}", response_model=List[SenhaResponse])
async def listar_senhas_usuario(user_id: int):
    """Lista todas as senhas de um usuário"""
    senhas = obter_senhas_usuario(user_id)
    return senhas

@router.get("/senha/melhor-tempo/{user_id}")
async def obter_melhor_tempo(user_id: int):
    """Obtém o melhor tempo de um usuário"""
    melhor_tempo = obter_melhor_tempo_usuario(user_id)
    if melhor_tempo is not None:
        return {"melhor_tempo": melhor_tempo}
    raise HTTPException(status_code=404, detail="Nenhuma senha encontrada para este usuário")

@router.get("/senha/estatisticas")
async def obter_estatisticas():
    """Obtém estatísticas globais do sistema"""
    return obter_estatisticas_globais()

@router.get("/senha/ranking")
async def obter_ranking():
    """Obtém o ranking global dos melhores tempos"""
    ranking = obter_ranking_global()
    return {"ranking": ranking}