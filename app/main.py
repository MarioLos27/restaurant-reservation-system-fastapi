from fastapi import FastAPI
from app.routers import clientes

app = FastAPI()

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])

"""
- Le añadimos un home para poder ver algo cuando se vaya a la pagina principal
- Este es un main de prueba, no esta terminado!!!
"""
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a La Mesa Dorada API"}