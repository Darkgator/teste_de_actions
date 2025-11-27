from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI()


class AssinaturaRequest(BaseModel):
    texto: str


class BpmnRequest(BaseModel):
    conteudo: str


class BpmnBase64Request(BaseModel):
    conteudo_base64: str


class BpmnResponse(BaseModel):
    conteudo: str


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/assinatura", response_model=AssinaturaRequest)
def assinar_texto(body: AssinaturaRequest):
    """
    Endpoint antigo, só para texto, mantém para compatibilidade.
    """
    return AssinaturaRequest(texto=body.texto + " ASSINATURA FODA REALIZADA 123456")


@app.post("/bpmn", response_model=BpmnResponse)
def ecoar_bpmn(body: BpmnRequest):
    """
    Endpoint antigo, recebe XML em texto puro e devolve igual.
    Útil para testes via Swagger.
    """
    return BpmnResponse(conteudo=body.conteudo)


@app.post("/bpmn_base64", response_model=BpmnResponse)
def ecoar_bpmn_base64(body: BpmnBase64Request):
    """
    Novo endpoint, recebe o arquivo BPMN em Base64,
    decodifica para texto e devolve o conteúdo exatamente igual.
    Esse é o endpoint que o Custom GPT deve usar para arquivos .bpmn.
    """
    try:
        # Decodifica a string Base64 para bytes
        raw_bytes = base64.b64decode(body.conteudo_base64)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Falha ao decodificar Base64, verifique se 'conteudo_base64' está correto."
        )

    # Tenta primeiro UTF 8
    texto = None
    errors = []

    for encoding in ["utf-8", "utf-16", "latin-1"]:
        try:
            texto = raw_bytes.decode(encoding)
            break
        except UnicodeDecodeError as e:
            errors.append(f"{encoding}: {str(e)}")

    if texto is None:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível decodificar o conteúdo em texto, tent
