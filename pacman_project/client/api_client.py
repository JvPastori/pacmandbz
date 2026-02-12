import requests

API_URL = "http://127.0.0.1:8000"  # Endereço do servidor FastAPI

def enviar_evento(tipo, detalhes=None):
    """
    Envia um evento para o servidor
    e retorna o estado atualizado do jogo.
    """
    try:
        data = {"type": tipo, "details": detalhes or {}}
        response = requests.post(f"{API_URL}/event", json=data)
        response.raise_for_status()  # lança erro se status != 200
        return response.json()  # retorna o JSON do servidor
    
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao enviar evento: {e}")
        return None

def obter_estado():
    """Busca o estado atual do jogo no servidor."""
    try:
        response = requests.get(f"{API_URL}/state")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao buscar estado: {e}")
        return None
