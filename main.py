from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BpmnRequest(BaseModel):
    conteudo: str

class BpmnResponse(BaseModel):
    conteudo: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/bpmn", response_model=BpmnResponse)
def processar_bpmn(body: BpmnRequest):
    return {"conteudo": body.conteudo}
