import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Testa o registro de usuário com sucesso
def test_register_user_success(client: TestClient, sample_user):
    
    response = client.post("/register", json=sample_user)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["msg"] == "Usuário cadastrado com sucesso"
    assert data["nome"] == sample_user["nome"]
    assert "id" in data

def test_register_user_duplicate_email(client: TestClient, sample_user):
    """Testa tentativa de registro com email duplicado"""
    # Primeiro registro
    client.post("/register", json=sample_user)
    
    # Segundo registro com mesmo email
    response = client.post("/register", json=sample_user)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email já cadastrado"

def test_register_user_invalid_email(client: TestClient):
    """Testa registro com email inválido"""
    invalid_user = {
        "nome": "João Silva",
        "email": "email_invalido"
    }
    
    response = client.post("/register", json=invalid_user)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_register_user_missing_fields(client: TestClient):
    """Testa registro com campos obrigatórios faltando"""
    incomplete_user = {
        "nome": "João Silva"
        # email faltando
    }
    
    response = client.post("/register", json=incomplete_user)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_register_user_empty_name(client: TestClient):
    """Testa registro com nome vazio"""
    user_empty_name = {
        "nome": "",
        "email": "teste@email.com"
    }
    
    response = client.post("/register", json=user_empty_name)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
