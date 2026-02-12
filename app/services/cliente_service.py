from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import ClienteDB, ClienteCreate, ClienteUpdate


def obtener_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClienteDB).offset(skip).limit(limit).all()


def obtener_por_id(db: Session, cliente_id: int):
    return db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()


def buscar_clientes(db: Session, texto: str):
    # Busca por nombre O email O teléfono
    texto_busqueda = f"%{texto}%"
    return db.query(ClienteDB).filter(
        or_(
            ClienteDB.nombre.ilike(texto_busqueda),
            ClienteDB.email.ilike(texto_busqueda),
            ClienteDB.telefono.ilike(texto_busqueda)
        )
    ).all()


def crear_cliente(db: Session, cliente_in: ClienteCreate):
    # Convertimos el esquema Pydantic a Modelo DB
    db_cliente = ClienteDB(**cliente_in.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)  # Recargamos para tener el ID y la fecha generados
    return db_cliente


def actualizar_cliente(db: Session, cliente_id: int, cliente_in: ClienteUpdate):
    db_cliente = obtener_por_id(db, cliente_id)
    if not db_cliente:
        return None

    # Actualizamos solo los campos que vengan con valor (no None)
    datos_actualizar = cliente_in.model_dump(exclude_unset=True)
    for key, value in datos_actualizar.items():
        setattr(db_cliente, key, value)

    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def eliminar_cliente(db: Session, cliente_id: int):
    db_cliente = obtener_por_id(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False