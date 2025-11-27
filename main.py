from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class AssinaturaRequest(BaseModel):
    texto: str


class BpmnRequest(BaseModel):
    conteudo: str


class BpmnResponse(BaseModel):
    conteudo: str


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/assinatura", response_model=AssinaturaRequest)
def assinar_texto(body: AssinaturaRequest):
    # Endpoint antigo, se ainda quiser usar assinatura em texto
    return AssinaturaRequest(texto=body.texto + " ASSINATURA FODA REALIZADA 123456")


@app.post("/bpmn", response_model=BpmnResponse)
def ecoar_bpmn(body: BpmnRequest):
    # Endpoint usado pela Action do Custom GPT
    # Apenas devolve exatamente o mesmo conteudo recebido
    return BpmnResponse(conteudo=body.conteudo)
