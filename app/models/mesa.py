from pydantic import BaseModel, Field
from typing import Optional, Literal


class Mesa(BaseModel):
    id: Optional[int] = None
    # ge y le para definir el minimo y el maximo de mesas que puede haber
    numero: int = Field(..., ge=1, le=99, description="Número de mesa del 1 al 99")
    capacidad: Literal[2, 4, 6, 8] # Uso literal para que la capacidad esté predefinida
    ubicacion: Literal["interior", "terraza", "privado"]
    activa: bool = True