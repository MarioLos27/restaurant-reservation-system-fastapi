import sqlite3
from sqlite3 import Connection
from datetime import datetime, timedelta
from app.models import ReservaCreate, ReservaUpdate
# Importamos nuestras excepciones personalizadas
from app.exceptions import (
    ClienteNoEncontradoError,
    MesaNoDisponibleError,
    ReservaSolapadaError,
    CapacidadExcedidaError,
    FueraDeHorarioError,
    CancelacionNoPermitidaError
)

# Metodo para obtener todas las reservas
def obtener_todas(conn: Connection, fecha: str = None, cliente_id: int = None):
    cursor = conn.cursor()
    query = "SELECT * FROM reservas"
    params = []
    conditions = []
    
    if fecha:
        # En SQLite, las fechas se guardan como string, uso la función date() de SQLite para comparar solo la parte de la fecha
        conditions.append("date(fecha_hora_inicio) = date(?)")
        params.append(fecha)
        
    if cliente_id:
        conditions.append("cliente_id = ?")
        params.append(cliente_id)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    cursor.execute(query, params)
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]

# Metodo para obtener una reserva por su ID
def obtener_por_id(conn: Connection, reserva_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
    fila = cursor.fetchone()
    return dict(fila) if fila else None

# Metodo para crear una reserva por su ID
def crear_reserva(conn: Connection, reserva_in: ReservaCreate):
    cursor = conn.cursor()

    # Horario de operación
    hora = reserva_in.fecha_hora_inicio.hour
    if not ((12 <= hora < 16) or (20 <= hora <= 23)):
        raise FueraDeHorarioError("El restaurante abre de 12:00-16:00 y 20:00-00:00")

    # Cliente existente
    cursor.execute("SELECT id FROM clientes WHERE id = ?", (reserva_in.cliente_id,))
    if not cursor.fetchone():
        raise ClienteNoEncontradoError(f"No existe el cliente con ID {reserva_in.cliente_id}")

    # Validar Mesa
    cursor.execute("SELECT * FROM mesas WHERE id = ?", (reserva_in.mesa_id,))
    mesa = cursor.fetchone()
    if not mesa:
        raise MesaNoDisponibleError(f"No existe la mesa con ID {reserva_in.mesa_id}")
    
    # Convertimos mesa a dict para acceder fácil
    mesa = dict(mesa)

    # Mesa activa
    if not mesa["activa"]:
        raise MesaNoDisponibleError("La mesa no está activa/habilitada")

    # Capacidad
    if reserva_in.num_comensales > mesa["capacidad"]:
        raise CapacidadExcedidaError(f"La mesa solo acepta {mesa['capacidad']} personas")

    # Solapamiento
    cursor.execute("""
        SELECT id FROM reservas
        WHERE mesa_id = ?
        AND estado != 'cancelada'
        AND fecha_hora_inicio < ?
        AND fecha_hora_fin > ?
    """, (reserva_in.mesa_id, reserva_in.fecha_hora_fin, reserva_in.fecha_hora_inicio))

    if cursor.fetchone():
        raise ReservaSolapadaError("La mesa ya está ocupada en ese horario")

    # Crear Reserva
    cursor.execute("""
        INSERT INTO reservas (cliente_id, mesa_id, fecha_hora_inicio, fecha_hora_fin, num_comensales, estado, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        reserva_in.cliente_id, 
        reserva_in.mesa_id, 
        reserva_in.fecha_hora_inicio, 
        reserva_in.fecha_hora_fin, 
        reserva_in.num_comensales, 
        reserva_in.estado, 
        reserva_in.notas
    ))
    conn.commit()
    
    nuevo_id = cursor.lastrowid
    
    # Devolver dict
    return {
        "id": nuevo_id,
        **reserva_in.model_dump(),
        "fecha_creacion": datetime.now()
    }

# Metodo para actualizar una reserva ya existente
def actualizar_reserva(conn: Connection, reserva_id: int, reserva_in: ReservaUpdate):
    reserva_actual = obtener_por_id(conn, reserva_id)
    if not reserva_actual:
        return None

    datos = reserva_in.model_dump(exclude_unset=True)
    if not datos:
        return reserva_actual

    # Recalcular fecha fin si cambia el inicio
    if "fecha_hora_inicio" in datos:
        nueva_inicio = datos["fecha_hora_inicio"]
        datos["fecha_hora_fin"] = nueva_inicio + timedelta(hours=2)

    cursor = conn.cursor()
    set_clauses = []
    values = []
    for key, value in datos.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    values.append(reserva_id)
    query = f"UPDATE reservas SET {', '.join(set_clauses)} WHERE id = ?"
    
    cursor.execute(query, values)
    conn.commit()
    
    return obtener_por_id(conn, reserva_id)

# Metodo para cambiar el estado de la reserva
def cambiar_estado(conn: Connection, reserva_id: int, nuevo_estado: str):
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM reservas WHERE id = ?", (reserva_id,))
    if not cursor.fetchone():
        return None

    cursor.execute("UPDATE reservas SET estado = ? WHERE id = ?", (nuevo_estado, reserva_id))
    conn.commit()
    
    return obtener_por_id(conn, reserva_id)

# Metodo para eliminar una reserva
def eliminar_reserva(conn: Connection, reserva_id: int):
    # REGLA 7: Cancelación controlada (Soft Delete)
    reserva = obtener_por_id(conn, reserva_id)
    if not reserva:
        return False

    if reserva["estado"] not in ["pendiente", "confirmada"]:
        raise CancelacionNoPermitidaError(f"No se puede cancelar una reserva en estado '{reserva['estado']}'")

    cambiar_estado(conn, reserva_id, "cancelada")
    return True