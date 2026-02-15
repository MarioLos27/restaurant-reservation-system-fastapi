# Este paquete centraliza todas las excepciones de negocio del sistema

from .custom_exceptions import (
    ClienteNoEncontradoError,
    MesaNoDisponibleError,
    ReservaSolapadaError,
    CapacidadExcedidaError,
    FueraDeHorarioError,
    CancelacionNoPermitidaError
)