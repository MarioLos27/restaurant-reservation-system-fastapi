# todas las excepciones

class ClienteNoEncontradoError(Exception):
    """El cliente especificado no existe"""
    pass

class MesaNoDisponibleError(Exception):
    """La mesa no está disponible en el horario solicitado o no está activa"""
    pass

class ReservaSolapadaError(Exception):
    """Ya existe una reserva para esa mesa en ese horario"""
    pass

class CapacidadExcedidaError(Exception):
    """El número de comensales excede la capacidad de la mesa"""
    pass

class FueraDeHorarioError(Exception):
    """La reserva está fuera del horario de operación"""
    pass

class CancelacionNoPermitidaError(Exception):
    """La reserva no puede cancelarse (muy tarde o estado inválido)"""
    pass