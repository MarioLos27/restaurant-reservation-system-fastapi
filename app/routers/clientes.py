from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from sqlite3 import Connection
from app.database import get_db
from app.models import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services import cliente_service

router = APIRouter()

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Connection = Depends(get_db)
):
    """
    Obtiene el listado de todos los clientes registrados en el sistema.
    Permite paginación mediante 'skip' y 'limit'.
    """
    return cliente_service.obtener_todos(db, skip, limit)

@router.get("/buscar/", response_model=List[ClienteResponse])
def buscar_clientes(
    q: str = Query(..., description="Nombre, email o teléfono"),
    db: Connection = Depends(get_db)
):
    """
    Busca clientes que coincidan con el término proporcionado.
    La búsqueda se realiza sobre el nombre, email o teléfono de forma insensible a mayúsculas.
    """
    return cliente_service.buscar_clientes(db, q)

@router.get("/{id}", response_model=ClienteResponse)
def obtener_cliente(id: int, db: Connection = Depends(get_db)):
    """
    Obtiene los detalles de un cliente específico buscando por su ID único.
    Si no existe, devuelve un error 404.
    """
    cliente = cliente_service.obtener_por_id(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Connection = Depends(get_db)):
    """
    Registra un nuevo cliente en la base de datos.
    El modelo valida automáticamente que el email sea válido y el teléfono tenga 9 dígitos.
    """
    # Si el email ya existe, el propio SQLite lanzará un error de integridad que el servicio maneja.
    try:
        return cliente_service.crear_cliente(db, cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=ClienteResponse)
def actualizar_cliente(id: int, cliente: ClienteUpdate, db: Connection = Depends(get_db)):
    """
    Actualiza la información de un cliente existente.
    Solo se modifican los campos que se envíen con valor, es decir no nulos.
    """
    resultado = cliente_service.actualizar_cliente(db, id, cliente)
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return resultado

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(id: int, db: Connection = Depends(get_db)):
    """
    Elimina un cliente del sistema.
    Si el cliente tiene reservas activas, podría fallar dependiendo de la configuración de la BD.
    """
    try:
        exito = cliente_service.eliminar_cliente(db, id)
        if not exito:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None