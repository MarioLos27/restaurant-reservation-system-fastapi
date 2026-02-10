# app/routers/clientes.py
from fastapi import APIRouter
from typing import List
from app.models.cliente import Cliente
from app.services import cliente_service

router = APIRouter()

# GET /clientes/
@router.get("/", response_model=List[Cliente])
def listar_clientes():
    return cliente_service.obtener_todos_los_clientes()