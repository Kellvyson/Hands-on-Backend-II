from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
import time

app = FastAPI()


@app.get("/legado")
def sistema_legado(x_legado_key: str = Header(None)):
    # valida o header
    if x_legado_key != "1234":
        raise HTTPException(status_code=401, detail="Chave invalida")
    
    # simula delay de sistema antigo
    time.sleep(2)
    
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <produto>
        <codigo>001</codigo>
        <nome>Teclado Mecanico</nome>
        <preco>299.90</preco>
        <estoque>45</estoque>
        <categoria>Perifericos</categoria>
        <datacadastro>2020-03-15</datacadastro>
    </produto>
    """
    
    return Response(content=xml, media_type="application/xml")