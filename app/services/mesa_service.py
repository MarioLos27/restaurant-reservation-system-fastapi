from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import MesaDB, MesaCreate, MesaUpdate, ReservaDB


def obtener_todas(db: Session):
    return db.query(MesaDB).all()


def obtener_por_id(db: Session, mesa_id: int):
    return db.query(MesaDB).filter(MesaDB.id == mesa_id).first()


def crear_mesa(db: Session, mesa_in: MesaCreate):
    # Verificar si el número ya existe
    existe = db.query(MesaDB).filter(MesaDB.numero == mesa_in.numero).first()
    if existe:
        raise ValueError(f"Ya existe una mesa con el número {mesa_in.numero}")

    db_mesa = MesaDB(**mesa_in.model_dump())
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa


def actualizar_mesa(db: Session, mesa_id: int, mesa_in: MesaUpdate):
    db_mesa = obtener_por_id(db, mesa_id)
    if not db_mesa:
        return None

    datos = mesa_in.model_dump(exclude_unset=True)
    for key, value in datos.items():
        setattr(db_mesa, key, value)

    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa


def eliminar_mesa(db: Session, mesa_id: int):
    db_mesa = obtener_por_id(db, mesa_id)
    if db_mesa:
        # Opcional: Verificar si tiene reservas futuras antes de borrar
        db.delete(db_mesa)
        db.commit()
        return True
    return False


def buscar_disponibles(db: Session, fecha_hora: datetime, comensales: int):
    # Calculamos el fin del turno (asumimos 2 horas por defecto para la búsqueda)
    fecha_fin_busqueda = fecha_hora + timedelta(hours=2)

    # Encontrar mesas OCUPADAS en ese rango de tiempo
    # Una mesa está ocupada si hay una reserva que empiece antes de que yo termine
    #  Y termine después de que yo empiece.
    subquery_ocupadas = db.query(ReservaDB.mesa_id).filter(
        ReservaDB.estado != "cancelada",
        ReservaDB.fecha_hora_inicio < fecha_fin_busqueda,
        ReservaDB.fecha_hora_fin > fecha_hora
    )

    # Seleccionar mesas que:
    # - Tengan capacidad suficiente
    # - Estén activas
    # - Su ID NO esté en la lista de ocupadas
    mesas_libres = db.query(MesaDB).filter(
        MesaDB.capacidad >= comensales,
        MesaDB.activa == True,
        ~MesaDB.id.in_(subquery_ocupadas)  # El símbolo ~ niega la condición (NOT IN)
    ).all()

    return mesas_libres