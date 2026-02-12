from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ReservaCreate, ReservaResponse, ReservaUpdate
from app.services import reserva_service

router = APIRouter()

@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    """
    Lista todas las reservas registradas en el sistema.
    """
    return reserva_service.obtener_todas(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReservaResponse)
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva reserva validando:
    - Existencia de cliente y mesa.
    - Disponibilidad de horario (no solapamiento).
    - Capacidad de la mesa.
    """
    return reserva_service.crear_reserva(db, reserva)

@router.get("/{id}", response_model=ReservaResponse)
def obtener_reserva(id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de una reserva por su ID.
    """
    reserva = reserva_service.obtener_por_id(db, id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.put("/{id}", response_model=ReservaResponse)
def modificar_reserva(id: int, reserva: ReservaUpdate, db: Session = Depends(get_db)):
    """
    Modifica una reserva existente (fecha, comensales, notas).
    Recalcula la hora de fin si se cambia la hora de inicio.
    """
    resultado = reserva_service.actualizar_reserva(db, id, reserva)
    if not resultado:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return resultado

@router.delete("/{id}")
def cancelar_reserva(id: int, db: Session = Depends(get_db)):
    """
    Cancela una reserva (Soft Delete).
    Cambia el estado a 'cancelada' si cumple las reglas de negocio.
    """
    if not reserva_service.eliminar_reserva(db, id):
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"mensaje": "Reserva cancelada"}

@router.patch("/{id}/confirmar", response_model=ReservaResponse)
def confirmar_reserva(id: int, db: Session = Depends(get_db)):
    """
    Cambia el estado de una reserva a 'confirmada'.
    """
    reserva = reserva_service.cambiar_estado(db, id, "confirmada")
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.patch("/{id}/completar", response_model=ReservaResponse)
def completar_reserva(id: int, db: Session = Depends(get_db)):
    """
    Marca una reserva como 'completada' (el cliente asistió).
    """
    reserva = reserva_service.cambiar_estado(db, id, "completada")
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva