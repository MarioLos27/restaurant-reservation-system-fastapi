from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

# Clase cliente
class Cliente(BaseModel):
    """
       Crea un nuevo usuario.

       - **id**: Autogenerado
       - **nombre**: Nombre del cliente, tamaño min 3 letras
       - **email**: email del cliente
       - **telefono**: Telefono del cliente, tamaño fijo predefino de 9 dígitos
       - **fecha_registro**: Fecha de registro del cliente, pilla la fecha automáticamente
       """
    id: Optional[int] = None
    nombre: str = Field(..., min_length=3)
    email: EmailStr
    telefono: str = Field(..., min_length=9, max_length=9, description="Debe tener 9 dígitos")
    fecha_registro: datetime = Field(default_factory=datetime.now)
