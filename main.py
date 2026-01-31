from fastapi import FastAPI
import requests
import xmltodict
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

# config do sistema legado
LEGADO_URL = "http://localhost:8001/legado"


@app.get("/adaptado")
def adaptar_legado():
    """Pega dados do sistema legado (XML) e converte pra JSON"""
    
    try:
        resp = requests.get(
            LEGADO_URL,
            headers={"X-Legado-Key": "1234"},
            timeout=5
        )
        resp.raise_for_status()
        
        # converte xml pra dict
        dados = xmltodict.parse(resp.text)
        produto = dados["produto"]
        
        return {
            "id": produto["codigo"],
            "nome": produto["nome"],
            "preco": float(produto["preco"]),
            "estoque": int(produto["estoque"])
        }
    
    except requests.exceptions.Timeout:
        return {"erro": "Sistema legado demorou demais"}
    
    except requests.exceptions.ConnectionError:
        return {"erro": "Sistema legado fora do ar"}
    
    except:
        return {"erro": "Falha ao conectar com sistema legado"}
    
# lista pra guardar eventos processados
eventos_processados = []
ids_processados = set()


@app.post("/webhook")
def receber_webhook(evento: dict):
    # valida campos obrigatórios
    if "tipo" not in evento or "pedido_id" not in evento:
        return {"erro": "Falta tipo ou pedido_id"}
    
    # valida segredo
    if evento.get("segredo") != "meusegredo123":
        return {"erro": "Não autorizado"}
    
    pedido_id = evento["pedido_id"]
    
    # checa se já processou (idempotência)
    if pedido_id in ids_processados:
        print(f"[WEBHOOK] Evento duplicado ignorado - Pedido {pedido_id}")
        return {"mensagem": "Evento já processado", "pedido_id": pedido_id}
    
    # salva o evento
    ids_processados.add(pedido_id)
    eventos_processados.append({
        "tipo": evento["tipo"],
        "pedido_id": pedido_id
    })
    
    print(f"[WEBHOOK] Novo evento: {evento['tipo']} - Pedido {pedido_id}")
    
    return {"mensagem": "Evento processado", "pedido_id": pedido_id}


@app.get("/eventos")
def listar_eventos():
    return {"total": len(eventos_processados), "eventos": eventos_processados}