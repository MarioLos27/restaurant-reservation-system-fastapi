from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional, Literal


class Reserva(BaseModel):
    id: Optional[int] = None
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    id_cliente: int
    id_mesa: int

    # Comprobamos que el numero sea positivo
    num_comensales: int = Field(..., gt=0, description="Al menos 1 persona")
    estado: Literal["pendiente", "confirmada", "completada", "cancelada"] = "pendiente"
    fecha_inicio: datetime

    # Esta variable tiene que ser Opcional porque la calcularemos nosotros automáticamente
    fecha_fin: Optional[datetime] = None

    # Método para validar que la fecha sea futura
    @field_validator('fecha_inicio')
    @classmethod
    def validar_futuro(cls, v):
        if v < datetime.now():
            raise ValueError("La fecha de reserva debe ser futura")
        return v

    # Método para calcular fecha fin automáticamente
    @model_validator(mode='after')
    def calcular_fecha_fin(self):
        # Si tenemos fecha de inicio, sumamos 2 horas automáticamente
        if self.fecha_inicio:
            self.fecha_fin = self.fecha_inicio + timedelta(hours=2)
        return self