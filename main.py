from fastapi import FastAPI
import requests

app = FastAPI()

# URL da PokéAPI
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"


@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}


@app.get("/externo/{pokemon}")
def buscar_pokemon(pokemon: str):
    """Busca dados de um pokemon na PokéAPI"""
    
    # fallback pra quando a API falhar
    fallback = {
        "nome": "Desconhecido",
        "mensagem": "Não foi possível buscar os dados do pokemon"
    }
    
    try:
        # faz a requisição com timeout de 3 segundos
        resp = requests.get(f"{POKEAPI_URL}{pokemon.lower()}", timeout=3)
        resp.raise_for_status()
        dados = resp.json()
        
        # pega só o que interessa
        resultado = {
            "nome": dados["name"],
            "id": dados["id"],
            "altura": dados["height"],
            "peso": dados["weight"],
            "sprite": dados["sprites"]["front_default"],
            "tipos": [t["type"]["name"] for t in dados["types"]]
        }
        
        return resultado
    
    except requests.exceptions.Timeout:
        return {**fallback, "erro": "API demorou demais pra responder"}
    
    except requests.exceptions.HTTPError:
        return {**fallback, "erro": "Pokemon não encontrado"}
    
    except requests.exceptions.ConnectionError:
        return {**fallback, "erro": "Sem conexão com a internet"}
    
    except Exception as e:
        return {**fallback, "erro": str(e)}