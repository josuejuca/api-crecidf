from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

CRECI_API_HOST = "https://api.crecidf.gov.br"

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
        raise HTTPException(status_code=404, detail="Erro ao validar o CRECI.")
    
    creci_data["userId"] = user_id
    return creci_data

@app.post("/buscar_corretor/", tags=["CRECI – DF"])
def buscar_corretor(consulta: str = Query(..., description="Número de CRECI, nome, CPF ou CNPJ do corretor")):
    try:
        url = f"{CRECI_API_HOST}/findBroker1"
        
        headers = {"Content-Type": "application/json"}
        data = {"captcha":"52422","query": consulta , "validator":"aAeC+AIroiNEAYG/d3gIZA==$92Z60McJFbNcoFzfyPfN7rPbV6wZdVFHWKycFAcOeZy3+pvWr0Bu4IwgEr3xHVHhstWa0bn0Vhk25SOVqz32yA=="}  # Enviando o valor no formato correto com 'query' 

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

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
