from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import clientes, mesas, reservas, estadisticas
from app.database import engine, Base
# Importamos todas las excepciones
from app.exceptions import (
    ClienteNoEncontradoError,
    MesaNoDisponibleError,
    ReservaSolapadaError,
    CapacidadExcedidaError,
    FueraDeHorarioError,
    CancelacionNoPermitidaError
)
# Importamos modelos Pydantic y DB para que se creen las tablas
from app.models import ClienteDB, MesaDB, ReservaDB

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="La Mesa Dorada API", version="1.0.0")

#  EXCEPTION HANDLERS

@app.exception_handler(ClienteNoEncontradoError)
async def cliente_no_encontrado_handler(request: Request, exc: ClienteNoEncontradoError):
    return JSONResponse(status_code=404, content={"message": str(exc)})

@app.exception_handler(MesaNoDisponibleError)
async def mesa_no_disponible_handler(request: Request, exc: MesaNoDisponibleError):
    return JSONResponse(status_code=409, content={"message": str(exc)}) # 409 Conflict

@app.exception_handler(ReservaSolapadaError)
async def reserva_solapada_handler(request: Request, exc: ReservaSolapadaError):
    return JSONResponse(status_code=409, content={"message": str(exc)}) # 409 Conflict

@app.exception_handler(CapacidadExcedidaError)
async def capacidad_excedida_handler(request: Request, exc: CapacidadExcedidaError):
    return JSONResponse(status_code=400, content={"message": str(exc)}) # 400 Bad Request

@app.exception_handler(FueraDeHorarioError)
async def fuera_de_horario_handler(request: Request, exc: FueraDeHorarioError):
    return JSONResponse(status_code=400, content={"message": str(exc)})

@app.exception_handler(CancelacionNoPermitidaError)
async def cancelacion_no_permitida_handler(request: Request, exc: CancelacionNoPermitidaError):
    return JSONResponse(status_code=400, content={"message": str(exc)})

# ----------------------------------------

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(mesas.router, prefix="/mesas", tags=["Mesas"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(estadisticas.router, prefix="/estadisticas", tags=["Estadísticas"])

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de La Mesa Dorada"}