# Archivo: app/database.py
import sqlite3
from sqlite3 import Connection

# Definimos la ruta donde se creará el archivo .db asumiendo que ejecutas el comando uvicorn desde la raíz del proyecto
DB_NAME = "data/restaurante.db"


#  Metodo para obtener la conexion de la base de datos, esta función se usará en los Routers
def get_db():
    conn = sqlite3.connect(DB_NAME)
    # Esto permite acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Metodo para crear las tablas al ejecutar
def init_db():
    """Crear tablas usando SQL al arrancar"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabla de clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefono TEXT NOT NULL,
        notas TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabla de mesas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER UNIQUE NOT NULL,
        capacidad INTEGER NOT NULL CHECK (capacidad IN (2, 4, 6, 8)),
        ubicacion TEXT NOT NULL CHECK (ubicacion IN ('interior', 'terraza', 'privado')),
        activa BOOLEAN DEFAULT 1
    );
    """)

    # Tabla de reservas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        mesa_id INTEGER NOT NULL,
        fecha_hora_inicio TIMESTAMP NOT NULL,
        fecha_hora_fin TIMESTAMP NOT NULL,
        num_comensales INTEGER NOT NULL,
        estado TEXT DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'confirmada', 'completada', 'cancelada')),
        notas TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (mesa_id) REFERENCES mesas (id)
    );
    """)

    # Indices para mejorar rendimiento
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_fecha ON reservas (fecha_hora_inicio);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_mesa ON reservas (mesa_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_cliente ON reservas (cliente_id);")
    
    conn.commit()
    conn.close()