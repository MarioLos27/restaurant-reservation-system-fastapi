from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import ReservaDB, ReservaCreate, ReservaUpdate, ClienteDB, MesaDB
# Importamos nuestras nuevas excepciones
from app.exceptions import (
    ClienteNoEncontradoError,
    MesaNoDisponibleError,
    ReservaSolapadaError,
    CapacidadExcedidaError,
    FueraDeHorarioError,
    CancelacionNoPermitidaError
)


def obtener_todas(db: Session):
    return db.query(ReservaDB).all()


def obtener_por_id(db: Session, reserva_id: int):
    return db.query(ReservaDB).filter(ReservaDB.id == reserva_id).first()


def crear_reserva(db: Session, reserva_in: ReservaCreate):
    # REGLA 3: Horario de operación ejemplo: 13:00 a 23:00
    hora = reserva_in.fecha_hora_inicio.hour
    if hora < 13 or hora > 23:
        raise FueraDeHorarioError("El restaurante solo abre de 13:00 a 23:00")

    #  REGLA 6: Cliente existente
    cliente = db.query(ClienteDB).filter(ClienteDB.id == reserva_in.cliente_id).first()
    if not cliente:
        raise ClienteNoEncontradoError(f"No existe el cliente con ID {reserva_in.cliente_id}")

    # Validar Mesa
    mesa = db.query(MesaDB).filter(MesaDB.id == reserva_in.mesa_id).first()
    if not mesa:
        # Usamos MesaNoDisponible si no existe, o podrías crear MesaNoEncontrada
        raise MesaNoDisponibleError(f"No existe la mesa con ID {reserva_in.mesa_id}")

    #   Mesa activa
    if not mesa.activa:
        raise MesaNoDisponibleError("La mesa no está activa/habilitada")

    # REGLA 2: Capacidad
    if reserva_in.num_comensales > mesa.capacidad:
        raise CapacidadExcedidaError(f"La mesa solo acepta {mesa.capacidad} personas")

    # REGLA 1: Solapamiento
    solapamiento = db.query(ReservaDB).filter(
        ReservaDB.mesa_id == reserva_in.mesa_id,
        ReservaDB.estado != "cancelada",
        ReservaDB.fecha_hora_inicio < reserva_in.fecha_hora_fin,
        ReservaDB.fecha_hora_fin > reserva_in.fecha_hora_inicio
    ).first()

    if solapamiento:
        raise ReservaSolapadaError("La mesa ya está ocupada en ese horario")

    # Crear Reserva
    db_reserva = ReservaDB(**reserva_in.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def actualizar_reserva(db: Session, reserva_id: int, reserva_in: ReservaUpdate):
    db_reserva = obtener_por_id(db, reserva_id)
    if not db_reserva:
        return None  # O lanzar error si prefieres

    datos = reserva_in.model_dump(exclude_unset=True)

    # Recalcular fecha fin si cambia el inicio
    if "fecha_hora_inicio" in datos:
        nueva_inicio = datos["fecha_hora_inicio"]
        datos["fecha_hora_fin"] = nueva_inicio + timedelta(hours=2)

    for key, value in datos.items():
        setattr(db_reserva, key, value)

    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def cambiar_estado(db: Session, reserva_id: int, nuevo_estado: str):
    db_reserva = obtener_por_id(db, reserva_id)
    if not db_reserva:
        return None

    db_reserva.estado = nuevo_estado
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def eliminar_reserva(db: Session, reserva_id: int):
    # REGLA 7: Cancelación controlada
    reserva = obtener_por_id(db, reserva_id)
    if not reserva:
        return False  # O lanzar error

    if reserva.estado not in ["pendiente", "confirmada"]:
        raise CancelacionNoPermitidaError(f"No se puede cancelar una reserva en estado '{reserva.estado}'")

    reserva.estado = "cancelada"
    db.add(reserva)
    db.commit()
    return True