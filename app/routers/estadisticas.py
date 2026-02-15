from fastapi import APIRouter, Depends
from sqlite3 import Connection
from datetime import date, datetime, timedelta
from app.database import get_db

router = APIRouter()

@router.get("/ocupacion/diaria")
def ocupacion_diaria(fecha: date, db: Connection = Depends(get_db)):
    """
    Calcula el porcentaje de ocupación del restaurante para una fecha específica.
    Basado en el número total de mesas y las reservas activas de ese día.
    """
    # Rango de fecha
    fecha_inicio_dia = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
    fecha_fin_dia = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)

    cursor = db.cursor()
    
    # Contar reservas en ese rango
    cursor.execute("""
        SELECT COUNT(*) FROM reservas 
        WHERE fecha_hora_inicio >= ? AND fecha_hora_inicio <= ? 
        AND estado != 'cancelada'
    """, (fecha_inicio_dia, fecha_fin_dia))
    reservas_count = cursor.fetchone()[0]

    # Contar total mesas
    cursor.execute("SELECT COUNT(*) FROM mesas")
    total_mesas = cursor.fetchone()[0]
    
    porcentaje = (reservas_count / total_mesas) * 100 if total_mesas > 0 else 0

    return {
        "fecha": fecha,
        "reservas_totales": reservas_count,
        "porcentaje_ocupacion": round(porcentaje, 2)
    }

@router.get("/resumen")
def resumen_general(db: Connection = Depends(get_db)):
    """
    Ofrece una visión global del estado del sistema:
    Total de reservas, clientes, mesas y un desglose de reservas por estado.
    """
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM reservas")
    total_reservas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM mesas")
    total_mesas = cursor.fetchone()[0]

    # Desglose por estado
    cursor.execute("SELECT estado, COUNT(*) FROM reservas GROUP BY estado")
    desglose = cursor.fetchall() # Lista de tuplas (estado, cuenta)
    desglose_dict = {row[0]: row[1] for row in desglose}

    return {
        "total_reservas_historico": total_reservas,
        "desglose_por_estado": desglose_dict,
        "total_clientes_registrados": total_clientes,
        "total_mesas_disponibles": total_mesas
    }

@router.get("/ocupacion/semanal")
def ocupacion_semanal(fecha_inicio: date, db: Connection = Depends(get_db)):
    """
    Ocupación de la semana, parámetro: fecha inicio
    """
    start = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day)
    end = start + timedelta(days=7)
    
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM reservas 
        WHERE fecha_hora_inicio >= ? AND fecha_hora_inicio < ?
        AND estado != 'cancelada'
    """, (start, end))
    reservas = cursor.fetchone()[0]
    
    return {"fecha_inicio": fecha_inicio, "fecha_fin": end.date(), "total_reservas": reservas}

@router.get("/clientes-frecuentes")
def clientes_frecuentes(db: Connection = Depends(get_db)):
    """
    Top 10 clientes con más reservas
    """
    cursor = db.cursor()
    # SQL JOIN manual
    cursor.execute("""
        SELECT c.nombre, COUNT(r.id) as total 
        FROM clientes c
        JOIN reservas r ON c.id = r.cliente_id
        GROUP BY c.id 
        ORDER BY total DESC 
        LIMIT 10
    """)
    resultado = cursor.fetchall()
    
    return [{"cliente": row[0], "reservas": row[1]} for row in resultado]

@router.get("/mesas-populares")
def mesas_populares(db: Connection = Depends(get_db)):
    """
    Mesas más reservadas
    """
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.numero, COUNT(r.id) as total 
        FROM mesas m
        JOIN reservas r ON m.id = r.mesa_id
        GROUP BY m.id 
        ORDER BY total DESC
    """)
    resultado = cursor.fetchall()
    
    return [{"mesa_numero": row[0], "reservas": row[1]} for row in resultado]