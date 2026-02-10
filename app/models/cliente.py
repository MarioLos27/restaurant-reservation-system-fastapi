from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class Cliente(BaseModel):
    id: Optional[int] = None
    nombre_completo: str = Field(..., min_length=3)
    email: EmailStr
    telefono: str = Field(..., min_length=9, max_length=9, description="Debe tener 9 dígitos")
    fecha_registro: datetime = Field(default_factory=datetime.now)
