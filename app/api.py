from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

CRECI_API_HOST = "https://api.crecidf.gov.br"
DEFAULT_HEADERS = {
    "Origin": "https://app.crecidf.gov.br",
    "Referer": "https://app.crecidf.gov.br/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "application/json",
}

@app.get("/")
def home():
    return {"message": "API CRECI DF | JUCA"}

@app.post("/creci_info/", tags=["CRECI – DF"])
def get_creci_info(creci_number: str):
    user_id = get_user_id_by_creci_number(creci_number)
    
    if not user_id:
        raise HTTPException(status_code=404, detail="CRECI não encontrado.")

    creci_data = verify_certificate(user_id)
    if not creci_data:
        raise HTTPException(status_code=502, detail="Erro ao validar o CRECI. Tente novamente mais tarde.")

    creci_data["userId"] = user_id
    return creci_data, {"certidaoregularidade": f"https://app.crecidf.gov.br/corretor/regularidade/{user_id}"}

@app.post("/buscar_corretor/", tags=["CRECI – DF"])
def buscar_corretor(consulta: str = Query(..., description="Número de CRECI, nome, CPF ou CNPJ do corretor")):
    url = f"{CRECI_API_HOST}/findBroker1"
    data = {
        "captcha": "52422",
        "query": consulta,
        "validator": "aAeC+AIroiNEAYG/d3gIZA==$92Z60McJFbNcoFzfyPfN7rPbV6wZdVFHWKycFAcOeZy3+pvWr0Bu4IwgEr3xHVHhstWa0bn0Vhk25SOVqz32yA=="
    }

    try:
        response = requests.post(url, headers=DEFAULT_HEADERS, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erro ao consultar corretor: {str(e)}")

def get_user_id_by_creci_number(creci_number: str) -> str | None:
    url = f"{CRECI_API_HOST}/getUserIdByCreciNumber"
    data = {"creciNumber": creci_number}

    try:
        response = requests.post(url, headers=DEFAULT_HEADERS, json=data, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        if json_data.get("ok"):
            return json_data.get("userId")
    except requests.exceptions.RequestException:
        pass
    return None

def verify_certificate(user_id: str) -> dict | None:
    url = f"{CRECI_API_HOST}/verifyCertificate"
    data = {"id": user_id}

    try:
        response = requests.post(url, headers=DEFAULT_HEADERS, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
