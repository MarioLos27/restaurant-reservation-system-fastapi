from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# MAIN PYDANTIC MODELS

# Base: Campos comunes (Input del usuario)
class ClienteBase(BaseModel):
    """Campos comunes"""
    nombre: str = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Email válido y único")
    telefono: str = Field(..., min_length=9, max_length=9, description="Teléfono español de 9 dígitos")
    notas: Optional[str] = Field(default=None, description="Preferencias opcionales")

# Create: Para crear (POST). Hereda de Base.
class ClienteCreate(ClienteBase):
    """Para crear un cliente (POST)"""
    pass

# Update: Para actualizar (PUT). Todos los campos son opcionales.
class ClienteUpdate(BaseModel):
    """Para actualizar un cliente (PUT) - todos opcionales"""
    nombre: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, min_length=9, max_length=9)
    notas: Optional[str] = None

# Response: Para respuestas (GET). Hereda de Base y añade campos de DB.
class ClienteResponse(ClienteBase):
    """Para respuestas (GET)"""
    id: int
    fecha_registro: datetime  