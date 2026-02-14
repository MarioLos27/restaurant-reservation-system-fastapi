from pydantic import BaseModel, Field
from typing import Optional, Literal

# MAIN PYDANTIC MODELS

# Base
class MesaBase(BaseModel):
    numero: int = Field(..., ge=1, le=99, description="Número único del 1 al 99")
    capacidad: Literal[2, 4, 6, 8] = Field(..., description="Solo 2, 4, 6 u 8")
    ubicacion: Literal["interior", "terraza", "privado"]
    activa: bool = Field(default=True, description="Si la mesa está disponible")

# Create (POST)
class MesaCreate(MesaBase):
    pass

# Update (PUT) - Todo opcional
class MesaUpdate(BaseModel):
    numero: Optional[int] = Field(default=None, ge=1, le=99)
    capacidad: Optional[Literal[2, 4, 6, 8]] = None
    ubicacion: Optional[Literal["interior", "terraza", "privado"]] = None
    activa: Optional[bool] = None

# Response (GET)
class MesaResponse(MesaBase):
    id: int