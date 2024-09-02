# api.py 
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

CRECI_API_HOST = "https://crecidf-api-002-2d82d2b4dcc1.herokuapp.com"

@app.get("/")
def home():
    return {"message":"API CRECI DF | JUCA"}

# Endpoint para receber o número CRECI e retornar as informações
@app.post("/creci_info/", tags=["CRECI – DF"])
def get_creci_info(creci_number: str):
    # 1. Transformar o número CRECI em userId
    user_id = get_user_id_by_creci_number(creci_number)
    
    if not user_id:
        raise HTTPException(status_code=404, detail="CRECI não encontrado.")
    
    # 2. Validar o userId
    creci_data = verify_certificate(user_id)
    
    if not creci_data:
        raise HTTPException(status_code=404, detail="Erro ao validar o CRECI.")
    
    # 3. Retornar os dados coletados
    return creci_data


def get_user_id_by_creci_number(creci_number: str) -> str:
    url = f"{CRECI_API_HOST}/getUserIdByCreciNumber"
    headers = {"Content-Type": "application/json"}
    data = {"creciNumber": creci_number}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200 and response.json().get("ok"):
        return response.json().get("userId")
    else:
        return None


def verify_certificate(user_id: str) -> dict:
    url = f"{CRECI_API_HOST}/verifyCertificate"
    headers = {"Content-Type": "application/json"}
    data = {"id": user_id}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
