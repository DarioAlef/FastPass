import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.schemas.models import Base
from app.utils.config import SessionLocal

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    # Criar as tabelas no banco de teste
    Base.metadata.create_all(bind=engine)
    
    # Sobrescrever a dependência do banco
    app.dependency_overrides[SessionLocal] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Limpar as tabelas após cada teste
    Base.metadata.drop_all(bind=engine)
    
    # Limpar os overrides
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user():

    return {
        "nome": "João Silva",
        "email": "joao@email.com"
    }

@pytest.fixture
def sample_password():
    # Fixture que retorna dados de uma senha de exemplo
    return {
        "senha": "MinhaSenh@123",
        "tempo_completado": 25,
        "user_id": 1  # Será atualizado nos testes
    }