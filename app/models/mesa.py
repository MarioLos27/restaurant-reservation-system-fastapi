from pydantic import BaseModel, Field
from typing import Optional, Literal

# Clase Mesa
class Mesa(BaseModel):
    """
           Crea un nuevo usuario.

           - **id**: Autogenerado
           - **numero**: Número de la mesa, tiene que ser entre el número 1 y el 99
           - **capacidad**: Capacidad de la mesa, se usa "literal" para que la capacidad tenga valores predefinidos
           - **ubicacion**: Ubicacion de la mesa, tiene literal también porque tiene 3 ubicaciones predefinidas
           - **activa**: Boolean para saber si la mesa está disponible o no
           """
    id: Optional[int] = None
    numero: int = Field(..., ge=1, le=99, description="Número de mesa del 1 al 99")
    capacidad: Literal[2, 4, 6, 8] # Uso literal para que la capacidad esté predefinida
    ubicacion: Literal["interior", "terraza", "privado"]
    activa: bool = True