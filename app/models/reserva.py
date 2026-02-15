from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional, Literal

# Base, Campos input básicos
class ReservaBase(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente existente")
    mesa_id: int = Field(..., description="ID de la mesa existente y activa")
    fecha_hora_inicio: datetime = Field(..., description="Debe ser futura")
    num_comensales: int = Field(..., gt=0)
    notas: Optional[str] = None

# Create POST Incluye validadores y campos con defaults al crear
class ReservaCreate(ReservaBase):
    estado: Literal["pendiente", "confirmada", "completada", "cancelada"] = "pendiente"
    # La fecha fin es calculada, no se recibe, pero la necesitamos en el objeto final
    fecha_hora_fin: Optional[datetime] = None

    @field_validator('fecha_hora_inicio')
    @classmethod
    def validar_futuro(cls, v):
        if v < datetime.now():
            raise ValueError("La fecha de reserva debe ser futura")
        return v

    @model_validator(mode='after')
    def calcular_fecha_fin(self):
        if self.fecha_hora_inicio:
            self.fecha_hora_fin = self.fecha_hora_inicio + timedelta(hours=2)
        return self

# Update PUT Normalmente solo se permite cambiar fecha, comensales o notas
class ReservaUpdate(BaseModel):
    fecha_hora_inicio: Optional[datetime] = None
    num_comensales: Optional[int] = Field(default=None, gt=0)
    notas: Optional[str] = None
    # Si cambian la fecha_inicio, en el service habrá que recalcular fecha_fin

# Response GET Incluye todo, más los campos autogenerados
class ReservaResponse(ReservaBase):
    id: int
    fecha_hora_fin: datetime # Aquí ya es obligatorio porque la DB lo tiene
    estado: str
    fecha_creacion: datetime # O str

    model_config = {
        "from_attributes": True
    }