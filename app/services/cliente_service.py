# app/services/cliente_service.py
from data.restaurante import lista_clientes

def obtener_todos_los_clientes():
    # Devolvemos la lista de clientes completa
    return lista_clientes