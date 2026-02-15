import sqlite3
from sqlite3 import Connection
from datetime import datetime, timedelta
from app.models import MesaCreate, MesaUpdate

# Metodo para obtener la lista de todas las mesas
def obtener_todas(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mesas")
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]

# Metodo para obtener una lista buscando por ID
def obtener_por_id(conn: Connection, mesa_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mesas WHERE id = ?", (mesa_id,))
    fila = cursor.fetchone()
    return dict(fila) if fila else None

# Metodo para crear una nueva mesa
def crear_mesa(conn: Connection, mesa_in: MesaCreate):
    cursor = conn.cursor()
    
    # Verificar si el número ya existe
    cursor.execute("SELECT id FROM mesas WHERE numero = ?", (mesa_in.numero,))
    if cursor.fetchone():
        raise ValueError(f"Ya existe una mesa con el número {mesa_in.numero}")

    cursor.execute("""
        INSERT INTO mesas (numero, capacidad, ubicacion, activa)
        VALUES (?, ?, ?, ?)
    """, (mesa_in.numero, mesa_in.capacidad, mesa_in.ubicacion, mesa_in.activa))
    conn.commit()
    
    nuevo_id = cursor.lastrowid
    
    return {
        "id": nuevo_id,
        "numero": mesa_in.numero,
        "capacidad": mesa_in.capacidad,
        "ubicacion": mesa_in.ubicacion,
        "activa": mesa_in.activa
    }

# Metodo para actualizar una mesa ya existente
def actualizar_mesa(conn: Connection, mesa_id: int, mesa_in: MesaUpdate):
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM mesas WHERE id = ?", (mesa_id,))
    if not cursor.fetchone():
        return None

    datos = mesa_in.model_dump(exclude_unset=True)
    if not datos:
        return obtener_por_id(conn, mesa_id)

    set_clauses = []
    values = []
    for key, value in datos.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    values.append(mesa_id)
    query = f"UPDATE mesas SET {', '.join(set_clauses)} WHERE id = ?"
    
    cursor.execute(query, values)
    conn.commit()
    
    return obtener_por_id(conn, mesa_id)

# Metodo para eliminar una mesa
def eliminar_mesa(conn: Connection, mesa_id: int):
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM mesas WHERE id = ?", (mesa_id,))
    if not cursor.fetchone():
        return False

    # Verificar si tiene reservas futuras
    ahora = datetime.now()
    cursor.execute("""
        SELECT id FROM reservas 
        WHERE mesa_id = ? AND fecha_hora_inicio > ?
    """, (mesa_id, ahora))

    if cursor.fetchone():
        raise ValueError("No se puede eliminar la mesa porque tiene reservas futuras")

    cursor.execute("DELETE FROM mesas WHERE id = ?", (mesa_id,))
    conn.commit()
    return True

# Metodo para buscar las mesas disponibles
def buscar_disponibles(conn: Connection, fecha_hora: datetime, comensales: int):
    cursor = conn.cursor()
    fecha_fin_busqueda = fecha_hora + timedelta(hours=2)

    # Lógica con SQL puro: Tengan capacidad suficiente, estén activas y no estén en la lista de mesas ocupadas en ese horario
    
    query = """
    SELECT * FROM mesas 
    WHERE capacidad >= ? 
    AND activa = 1
    AND id NOT IN (
        SELECT mesa_id FROM reservas
        WHERE estado != 'cancelada'
        AND fecha_hora_inicio < ?
        AND fecha_hora_fin > ?
    )
    """
    
    cursor.execute(query, (comensales, fecha_fin_busqueda, fecha_hora))
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]