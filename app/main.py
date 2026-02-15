import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import init_db, DB_NAME
from app.routers import clientes, mesas, reservas, estadisticas
# Importamos datos de prueba (desde la carpeta en la raíz)
from data.restaurante import lista_clientes, lista_mesas

# Importamos todas las excepciones
from app.exceptions import (
    ClienteNoEncontradoError,
    MesaNoDisponibleError,
    ReservaSolapadaError,
    CapacidadExcedidaError,
    FueraDeHorarioError,
    CancelacionNoPermitidaError
)

# Crear tablas
init_db()

# Instancia de la aplicación
app = FastAPI(title="La Mesa Dorada API", version="1.0.0")

# Eventos de arranque
@app.on_event("startup")
def startup_event():
    # Conexión directa para insertar datos iniciales
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Si no hay mesas, las creamos
        cursor.execute("SELECT COUNT(*) FROM mesas")
        if cursor.fetchone()[0] == 0:
            for mesa in lista_mesas:
                cursor.execute("""
                    INSERT INTO mesas (numero, capacidad, ubicacion, activa)
                    VALUES (?, ?, ?, ?)
                """, (mesa["numero"], mesa["capacidad"], mesa["ubicacion"], mesa["activa"]))
            conn.commit()
        
        # Si no hay clientes, los creamos
        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            for cliente in lista_clientes:
                cursor.execute("""
                    INSERT INTO clientes (nombre, email, telefono, notas)
                    VALUES (?, ?, ?, ?)
                """, (cliente["nombre"], cliente["email"], cliente["telefono"], cliente["notas"]))
            conn.commit()
            
    finally:
        conn.close()

# Exceptions handlers

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

# Routers

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(mesas.router, prefix="/mesas", tags=["Mesas"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(estadisticas.router, prefix="/estadisticas", tags=["Estadísticas"])

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de La Mesa Dorada"}