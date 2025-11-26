from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AssinaturaRequest(BaseModel):
    texto: str

class AssinaturaResponse(BaseModel):
    resultado: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/assinatura", response_model=AssinaturaResponse)
def criar_assinatura(body: AssinaturaRequest):
    texto_original = body.texto
    texto_assinado = f"{texto_original} ASSINATURA FODA REALIZADA 123456"
    return {"resultado": texto_assinado}
