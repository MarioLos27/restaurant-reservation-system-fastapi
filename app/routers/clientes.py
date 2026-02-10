from fastapi import APIRouter

router = APIRouter()

@router.get("/clientes/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return {
        "usuario_id": usuario_id,
        "nombre": f"Usuario {usuario_id}"
    }

