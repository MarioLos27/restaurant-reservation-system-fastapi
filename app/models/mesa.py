from pydantic import BaseModel, Field
from typing import Optional, Literal
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

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

    model_config = {
        "from_attributes": True
    }

# SQLALCHEMY DB MODEL
class MesaDB(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidad = Column(Integer, nullable=False)
    ubicacion = Column(String, nullable=False)
    activa = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("capacidad IN (2, 4, 6, 8)", name="check_capacidad"),
        CheckConstraint("ubicacion IN ('interior', 'terraza', 'privado')", name="check_ubicacion"),
    )

    reservas = relationship("ReservaDB", back_populates="mesa")