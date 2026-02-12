from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional, Literal
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# MAIN PYDANTIC MODELS

# Base: Campos input básicos
class ReservaBase(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente existente")
    mesa_id: int = Field(..., description="ID de la mesa existente y activa")
    fecha_hora_inicio: datetime = Field(..., description="Debe ser futura")
    num_comensales: int = Field(..., gt=0)
    notas: Optional[str] = None

# Create (POST): Incluye validadores y campos con defaults al crear
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

#  Update (PUT): Normalmente solo se permite cambiar fecha, comensales o notas
class ReservaUpdate(BaseModel):
    fecha_hora_inicio: Optional[datetime] = None
    num_comensales: Optional[int] = Field(default=None, gt=0)
    notas: Optional[str] = None
    # Nota: Si cambian la fecha_inicio, en el service habrá que recalcular fecha_fin

# Response (GET): Incluye todo, más los campos autogenerados
class ReservaResponse(ReservaBase):
    id: int
    fecha_hora_fin: datetime # Aquí ya es obligatorio porque la DB lo tiene
    estado: str
    fecha_creacion: datetime

    model_config = {
        "from_attributes": True
    }

# SQLALCHEMY DB MODEL
class ReservaDB(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)
    num_comensales = Column(Integer, nullable=False)
    estado = Column(String, default="pendiente")
    notas = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'confirmada', 'completada', 'cancelada')", name="check_estado"),
        Index("idx_reservas_fecha", "fecha_hora_inicio"),
        Index("idx_reservas_mesa", "mesa_id"),
        Index("idx_reservas_cliente", "cliente_id"),
    )

    cliente = relationship("ClienteDB", back_populates="reservas")
    mesa = relationship("MesaDB", back_populates="reservas")