import pytest
from fastapi.testclient import TestClient
from fastapi import status

def test_home_endpoint_returns_html(client: TestClient):
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "FastPass" in response.text
    assert "Desafio de senhas" in response.text
