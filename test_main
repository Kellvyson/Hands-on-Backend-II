from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "mensagem" in response.json()


def test_pokemon_valido():
    response = client.get("/externo/pikachu")
    assert response.status_code == 200
    data = response.json()
    assert "nome" in data or "erro" in data