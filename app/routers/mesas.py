from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from datetime import datetime
from sqlite3 import Connection
from app.database import get_db
from app.models import MesaCreate, MesaResponse, MesaUpdate
from app.services import mesa_service

router = APIRouter()

@router.get("/", response_model=List[MesaResponse])
def listar_mesas(db: Connection = Depends(get_db)):
    """
    Devuelve un listado completo de todas las mesas del restaurante.
    """
    return mesa_service.obtener_todas(db)

@router.get("/disponibles/", response_model=List[MesaResponse])
def buscar_mesas_disponibles(
    fecha: datetime,
    comensales: int = Query(..., gt=0),
    db: Connection = Depends(get_db)
):
    """
    Busca mesas que estén libres para una fecha y hora específicas,
    filtrando por la capacidad necesaria para los comensales.
    """
    return mesa_service.buscar_disponibles(db, fecha, comensales)

@router.get("/{id}", response_model=MesaResponse)
def obtener_mesa(id: int, db: Connection = Depends(get_db)):
    """
    Obtiene los datos de una mesa específica por su ID.
    """
    mesa = mesa_service.obtener_por_id(db, id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MesaResponse)
def crear_mesa(mesa: MesaCreate, db: Connection = Depends(get_db)):
    """
    Crea una nueva mesa en el sistema.
    Valida que el número de mesa no esté duplicado.
    """
    try:
        return mesa_service.crear_mesa(db, mesa)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mesa(id: int, db: Connection = Depends(get_db)):
    """
    Elimina una mesa específica por su ID.
    """
    try:
        exito = mesa_service.eliminar_mesa(db, id)
        if not exito:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None