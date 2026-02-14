import sqlite3
from sqlite3 import Connection
from app.models import ClienteCreate, ClienteUpdate

def obtener_todos(conn: Connection, skip: int = 0, limit: int = 100):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?", (limit, skip))
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]

def obtener_por_id(conn: Connection, cliente_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    fila = cursor.fetchone()
    return dict(fila) if fila else None

def buscar_clientes(conn: Connection, texto: str):
    # Busca por nombre O email O teléfono usando LIKE
    cursor = conn.cursor()
    texto_busqueda = f"%{texto}%"
    cursor.execute("""
        SELECT * FROM clientes 
        WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ?
    """, (texto_busqueda, texto_busqueda, texto_busqueda))
    filas = cursor.fetchall()
    return [dict(fila) for fila in filas]

def crear_cliente(conn: Connection, cliente_in: ClienteCreate):
    cursor = conn.cursor()
    # Insertar
    try:
        cursor.execute("""
            INSERT INTO clientes (nombre, email, telefono, notas)
            VALUES (?, ?, ?, ?)
        """, (cliente_in.nombre, cliente_in.email, cliente_in.telefono, cliente_in.notas))
        conn.commit()
        
        # Recuperar el ID generado
        nuevo_id = cursor.lastrowid
        
        # Devolver el objeto creado (construimos el diccionario manualmente o hacemos un SELECT)
        # Para ser rápidos, lo construimos:
        return {
            "id": nuevo_id,
            "nombre": cliente_in.nombre,
            "email": cliente_in.email,
            "telefono": cliente_in.telefono,
            "notas": cliente_in.notas,
            "fecha_registro": "Recién creado" # SQLite lo maneja internamente
        }
    except sqlite3.IntegrityError:
        # Si el email ya existe, SQLite lanzará error
        raise ValueError("El email ya está registrado")

def actualizar_cliente(conn: Connection, cliente_id: int, cliente_in: ClienteUpdate):
    cursor = conn.cursor()
    
    # Verificar si existe
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    if not cursor.fetchone():
        return None

    # Construir query dinámica
    datos = cliente_in.model_dump(exclude_unset=True)
    if not datos:
        return obtener_por_id(conn, cliente_id)

    set_clauses = []
    values = []
    for key, value in datos.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    values.append(cliente_id) # Para el WHERE
    query = f"UPDATE clientes SET {', '.join(set_clauses)} WHERE id = ?"
    
    cursor.execute(query, values)
    conn.commit()
    
    return obtener_por_id(conn, cliente_id)

def eliminar_cliente(conn: Connection, cliente_id: int):
    cursor = conn.cursor()
    
    # Verificar si existe
    cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
    if not cursor.fetchone():
        return False # No encontrado

    # Verificar si tiene reservas activas
    cursor.execute("""
        SELECT id FROM reservas 
        WHERE cliente_id = ? AND estado IN ('pendiente', 'confirmada')
    """, (cliente_id,))
    
    if cursor.fetchone():
        raise ValueError("No se puede eliminar un cliente con reservas activas")

    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    return True