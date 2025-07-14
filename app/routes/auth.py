from fastapi import status, APIRouter, HTTPException
from app.schemas.models import User
from app.services.new_user import create_user, get_user_by_email

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    db_user = create_user(user)
    if db_user:
        return {"msg": "Usuário cadastrado com sucesso", "id": db_user.id, "nome": db_user.nome}
    raise HTTPException(status_code=400, detail="Email já cadastrado")

@router.get("/user/{email}")
async def get_user(email: str):
    user = get_user_by_email(email)
    if user:
        return {"id": user.id, "nome": user.nome, "email": user.email}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")