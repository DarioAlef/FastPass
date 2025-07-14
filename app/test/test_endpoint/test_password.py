import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Testa salvamento de senha com sucesso
def test_salvar_senha_success(client: TestClient, sample_user, sample_password):
    
    # Primeiro registra o usuário
    user_response = client.post("/register", json=sample_user)
    user_id = user_response.json()["id"]
    
    # Atualiza o user_id na senha
    sample_password["user_id"] = user_id
    
    # Salva a senha
    response = client.post("/senha/salvar", json=sample_password)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["msg"] == "Senha salva com sucesso!"
    assert data["tempo_completado"] == sample_password["tempo_completado"]
    assert "id" in data