from fastapi import FastAPI

# Cria a aplicação
app = FastAPI()

# Define uma rota
@app.get("/")
def home():
    return {"message": "Servidor está rodando!"}
