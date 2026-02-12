# app/data/restaurante.py

# Listas vacías para clientes y reservas
lista_clientes = []
lista_reservas = []

# Pre-cargamos las 15 mesas según el enunciado
lista_mesas = [
    # 2 Personas (Mesas 1-5)
    {"id": 1, "numero": 1, "capacidad": 2, "ubicacion": "interior", "activa": True},
    {"id": 2, "numero": 2, "capacidad": 2, "ubicacion": "interior", "activa": True},
    {"id": 3, "numero": 3, "capacidad": 2, "ubicacion": "terraza", "activa": True},
    {"id": 4, "numero": 4, "capacidad": 2, "ubicacion": "terraza", "activa": True},
    {"id": 5, "numero": 5, "capacidad": 2, "ubicacion": "privado", "activa": True},
    # 4 Personas (Mesas 6-10)
    {"id": 6, "numero": 6, "capacidad": 4, "ubicacion": "interior", "activa": True},
    {"id": 7, "numero": 7, "capacidad": 4, "ubicacion": "interior", "activa": True},
    {"id": 8, "numero": 8, "capacidad": 4, "ubicacion": "terraza", "activa": True},
    {"id": 9, "numero": 9, "capacidad": 4, "ubicacion": "terraza", "activa": True},
    {"id": 10, "numero": 10, "capacidad": 4, "ubicacion": "interior", "activa": True},
    # 6 Personas (Mesas 11-13)
    {"id": 11, "numero": 11, "capacidad": 6, "ubicacion": "interior", "activa": True},
    {"id": 12, "numero": 12, "capacidad": 6, "ubicacion": "terraza", "activa": True},
    {"id": 13, "numero": 13, "capacidad": 6, "ubicacion": "interior", "activa": True},
    # 8 Personas (Mesas 14-15)
    {"id": 14, "numero": 14, "capacidad": 8, "ubicacion": "privado", "activa": True},
    {"id": 15, "numero": 15, "capacidad": 8, "ubicacion": "terraza", "activa": True},
]