from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from app.database import get_db
from app.models import ReservaDB, ClienteDB, MesaDB

router = APIRouter()


@router.get("/ocupacion/diaria")
def ocupacion_diaria(fecha: date, db: Session = Depends(get_db)):
    """
    Calcula el porcentaje de ocupación del restaurante para una fecha específica.
    Basado en el número total de mesas y las reservas activas de ese día.
    """
    fecha_inicio_dia = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
    fecha_fin_dia = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)

    reservas_count = db.query(ReservaDB).filter(
        ReservaDB.fecha_hora_inicio >= fecha_inicio_dia,
        ReservaDB.fecha_hora_inicio <= fecha_fin_dia,
        ReservaDB.estado != "cancelada"
    ).count()

    total_mesas = db.query(MesaDB).count()
    porcentaje = (reservas_count / total_mesas) * 100 if total_mesas > 0 else 0

    return {
        "fecha": fecha,
        "reservas_totales": reservas_count,
        "porcentaje_ocupacion": round(porcentaje, 2)
    }


@router.get("/resumen")
def resumen_general(db: Session = Depends(get_db)):
    """
    Ofrece una visión global del estado del sistema:
    Total de reservas, clientes, mesas y un desglose de reservas por estado.
    """
    total_reservas = db.query(ReservaDB).count()
    total_clientes = db.query(ClienteDB).count()
    total_mesas = db.query(MesaDB).count()

    desglose = db.query(ReservaDB.estado, func.count(ReservaDB.estado)).group_by(ReservaDB.estado).all()
    desglose_dict = {estado: cuenta for estado, cuenta in desglose}

    return {
        "total_reservas_historico": total_reservas,
        "desglose_por_estado": desglose_dict,
        "total_clientes_registrados": total_clientes,
        "total_mesas_disponibles": total_mesas
    }