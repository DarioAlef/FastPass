from fastapi import FastAPI
from app.routes.home import router as home_router
from app.routes.auth import router as auth_router
from app.routes.password import router as senha_router
from app.schemas.models import Base
from app.utils.config import engine
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="FastPass")

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static2")

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(senha_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )