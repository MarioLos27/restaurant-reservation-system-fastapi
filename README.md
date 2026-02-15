# API de Sistema de Reservas de Restaurante - La Mesa Dorada

## Descripción del Proyecto

API REST completa desarrollada con FastAPI para gestionar el sistema de reservas del restaurante "La Mesa Dorada". Este sistema permite modernizar la gestión de reservas tradicional basada en papel, proporcionando una solución digital robusta para manejar clientes, mesas y reservas de forma eficiente.

La API garantiza que no se produzcan conflictos de horarios, valida capacidades de mesas, respeta el horario de operación del restaurante y proporciona estadísticas de ocupación para ayudar a la gerencia en la toma de decisiones.

---

## Características del Restaurante

- **Horario de operación**: 
  - Comidas: 12:00 a 16:00
  - Cenas: 20:00 a 00:00
- **Capacidad**: 15 mesas de diferentes tamaños (2, 4, 6 y 8 personas)
- **Duración estándar de reserva**: 2 horas
- **Política de cancelación**: Las reservas pueden cancelarse hasta 2 horas antes

---

## Requisitos Previos

- **Python 3.8+** instalado en el sistema
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

---

## Instalación

### 1. Clonar o descargar el proyecto

Si tienes Git instalado:
```bash
git clone <url-del-repositorio>
cd reservas_restaurante
```

O simplemente descomprime el archivo ZIP en tu directorio de trabajo.

### 2. Crear un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `fastapi`: Framework web moderno para construir APIs
- `uvicorn`: Servidor ASGI de alto rendimiento
- `pydantic[email]`: Validación de datos y modelos con soporte para emails

---

## Cómo Ejecutar la Aplicación

### 1. Iniciar el servidor

Desde la raíz del proyecto, ejecuta:

```bash
uvicorn app.main:app --reload
```

El flag `--reload` permite que el servidor se reinicie automáticamente cuando detecta cambios en el código (útil para desarrollo).

### 2. Acceder a la aplicación

- **API disponible en**: http://127.0.0.1:8000
- **Documentación interactiva (Swagger UI)**: http://127.0.0.1:8000/docs
- **Documentación alternativa (ReDoc)**: http://127.0.0.1:8000/redoc

---

## Estructura del Proyecto

```
reservas_restaurante/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada de la aplicación
│   ├── database.py                # Configuración de la base de datos SQLite
│   │
│   ├── models/                    # Modelos Pydantic para validación
│   │   ├── __init__.py
│   │   ├── cliente.py            # Modelos de Cliente (Create, Update, Response)
│   │   ├── mesa.py               # Modelos de Mesa
│   │   └── reserva.py            # Modelos de Reserva
│   │
│   ├── routers/                   # Endpoints organizados por recurso
│   │   ├── __init__.py
│   │   ├── clientes.py           # CRUD de clientes + búsqueda
│   │   ├── mesas.py              # CRUD de mesas + disponibilidad
│   │   ├── reservas.py           # CRUD de reservas + confirmación/completado
│   │   └── estadisticas.py       # Endpoints de estadísticas y reportes
│   │
│   ├── services/                  # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── cliente_service.py    # Operaciones de clientes
│   │   ├── mesa_service.py       # Operaciones de mesas
│   │   └── reserva_service.py    # Operaciones de reservas + validaciones
│   │
│   └── exceptions/                # Excepciones personalizadas
│       ├── __init__.py
│       └── custom_exceptions.py  # Errores de negocio específicos
│
├── data/
│   ├── restaurante.db            # Base de datos SQLite (se crea automáticamente)
│   └── restaurante.py            # Datos de prueba iniciales
│
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Este archivo
└── .gitignore                    # Archivos ignorados por Git
```

### Descripción de los Componentes

- **main.py**: Configuración de la aplicación FastAPI, manejadores de excepciones y carga de datos iniciales
- **database.py**: Configuración de conexión a SQLite y creación de tablas
- **models/**: Modelos Pydantic separados por operación (Create, Update, Response) con validaciones
- **routers/**: Endpoints REST organizados por recurso con documentación
- **services/**: Lógica de negocio y reglas de validación separadas de los endpoints
- **exceptions/**: Excepciones personalizadas para errores específicos del negocio

---

## Ejemplos de Uso

### 1. Listar todos los clientes

```bash
GET http://127.0.0.1:8000/clientes/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Perez",
    "email": "juan@example.com",
    "telefono": "600111222",
    "notas": "Alergico nueces",
    "fecha_registro": "2024-02-14T10:30:00"
  },
  ...
]
```

### 2. Crear un nuevo cliente

```bash
POST http://127.0.0.1:8000/clientes/
Content-Type: application/json

{
  "nombre": "Roberto Sanchez",
  "email": "roberto@example.com",
  "telefono": "600987654",
  "notas": "Prefiere mesa junto a ventana"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 11,
  "nombre": "Roberto Sanchez",
  "email": "roberto@example.com",
  "telefono": "600987654",
  "notas": "Prefiere mesa junto a ventana",
  "fecha_registro": "2024-02-14T15:45:00"
}
```

### 3. Buscar mesas disponibles

```bash
GET http://127.0.0.1:8000/mesas/disponibles/?fecha=2024-12-20T20:00:00&comensales=4
```

**Respuesta:**
```json
[
  {
    "id": 6,
    "numero": 6,
    "capacidad": 4,
    "ubicacion": "interior",
    "activa": true
  },
  {
    "id": 7,
    "numero": 7,
    "capacidad": 4,
    "ubicacion": "interior",
    "activa": true
  }
]
```

### 4. Crear una reserva

```bash
POST http://127.0.0.1:8000/reservas/
Content-Type: application/json

{
  "cliente_id": 1,
  "mesa_id": 5,
  "fecha_hora_inicio": "2024-12-20T20:00:00",
  "num_comensales": 4,
  "notas": "Cumpleaños, traer tarta"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "id": 21,
  "cliente_id": 1,
  "mesa_id": 5,
  "fecha_hora_inicio": "2024-12-20T20:00:00",
  "fecha_hora_fin": "2024-12-20T22:00:00",
  "num_comensales": 4,
  "estado": "pendiente",
  "notas": "Cumpleaños, traer tarta",
  "fecha_creacion": "2024-12-15T10:30:00"
}
```

### 5. Confirmar llegada del cliente

```bash
PATCH http://127.0.0.1:8000/reservas/21/confirmar
```

**Respuesta:**
```json
{
  "id": 21,
  "cliente_id": 1,
  "mesa_id": 5,
  "fecha_hora_inicio": "2024-12-20T20:00:00",
  "fecha_hora_fin": "2024-12-20T22:00:00",
  "num_comensales": 4,
  "estado": "confirmada",
  "notas": "Cumpleaños, traer tarta",
  "fecha_creacion": "2024-12-15T10:30:00"
}
```

### 6. Obtener estadísticas de ocupación diaria

```bash
GET http://127.0.0.1:8000/estadisticas/ocupacion/diaria?fecha=2024-12-20
```

**Respuesta:**
```json
{
  "fecha": "2024-12-20",
  "reservas_totales": 12,
  "porcentaje_ocupacion": 80.0
}
```

### 7. Ver resumen general

```bash
GET http://127.0.0.1:8000/estadisticas/resumen
```

**Respuesta:**
```json
{
  "total_reservas_historico": 45,
  "desglose_por_estado": {
    "pendiente": 8,
    "confirmada": 5,
    "completada": 28,
    "cancelada": 4
  },
  "total_clientes_registrados": 10,
  "total_mesas_disponibles": 15
}
```

---

## Validaciones Implementadas

El sistema implementa las siguientes validaciones de negocio:

1. **No solapamiento de reservas**: Una mesa no puede tener dos reservas que se superpongan en el tiempo
2. **Capacidad de mesa**: El número de comensales no puede exceder la capacidad de la mesa
3. **Horario de operación**: Las reservas solo pueden hacerse dentro del horario del restaurante (12:00-16:00 y 20:00-00:00)
4. **Reservas futuras**: No se pueden crear reservas en el pasado
5. **Mesa activa**: Solo se pueden hacer reservas en mesas activas
6. **Cliente existente**: El cliente debe existir en la base de datos
7. **Cancelación**: Las reservas solo pueden cancelarse si están en estado "pendiente" o "confirmada"

---

## Manejo de Errores

La API utiliza excepciones personalizadas para comunicar errores de negocio de forma clara:

- **ClienteNoEncontradoError** (404): El cliente especificado no existe
- **MesaNoDisponibleError** (409): La mesa no está disponible o no está activa
- **ReservaSolapadaError** (409): Ya existe una reserva para esa mesa en ese horario
- **CapacidadExcedidaError** (400): El número de comensales excede la capacidad de la mesa
- **FueraDeHorarioError** (400): La reserva está fuera del horario de operación
- **CancelacionNoPermitidaError** (400): La reserva no puede cancelarse

**Ejemplo de respuesta de error:**
```json
{
  "message": "La mesa 5 ya está ocupada en ese horario"
}
```

---

## Datos de Prueba

Al iniciar la aplicación por primera vez, se cargan automáticamente:

- **10 clientes** de ejemplo con diferentes preferencias
- **15 mesas** distribuidas:
  - 5 mesas de 2 personas
  - 5 mesas de 4 personas
  - 3 mesas de 6 personas
  - 2 mesas de 8 personas

Los datos están ubicados en `data/restaurante.py` y se insertan automáticamente en la base de datos si está vacía.

---

## Endpoints Disponibles

### Clientes
- `GET /clientes/` - Listar todos los clientes (con paginación)
- `GET /clientes/{id}` - Obtener un cliente por ID
- `GET /clientes/buscar/?q={texto}` - Buscar clientes por nombre, email o teléfono
- `POST /clientes/` - Crear un nuevo cliente
- `PUT /clientes/{id}` - Actualizar datos de un cliente
- `DELETE /clientes/{id}` - Eliminar un cliente

### Mesas
- `GET /mesas/` - Listar todas las mesas
- `GET /mesas/{id}` - Obtener una mesa por ID
- `GET /mesas/disponibles/?fecha={fecha}&comensales={n}` - Buscar mesas disponibles
- `POST /mesas/` - Crear una nueva mesa
- `DELETE /mesas/{id}` - Eliminar una mesa

### Reservas
- `GET /reservas/` - Listar reservas con filtros
- `GET /reservas/{id}` - Obtener una reserva por ID
- `POST /reservas/` - Crear una nueva reserva
- `PUT /reservas/{id}` - Modificar una reserva
- `DELETE /reservas/{id}` - Cancelar una reserva
- `PATCH /reservas/{id}/confirmar` - Confirmar llegada del cliente
- `PATCH /reservas/{id}/completar` - Marcar reserva como completada

### Estadísticas
- `GET /estadisticas/ocupacion/diaria?fecha={fecha}` - Ocupación por día
- `GET /estadisticas/ocupacion/semanal?fecha_inicio={fecha}` - Ocupación semanal
- `GET /estadisticas/clientes-frecuentes` - Top 10 clientes con más reservas
- `GET /estadisticas/mesas-populares` - Mesas más reservadas
- `GET /estadisticas/resumen` - Resumen general del sistema

---

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs con Python
- **Pydantic**: Validación de datos utilizando type hints de Python
- **SQLite**: Base de datos relacional ligera y sin servidor
- **Uvicorn**: Servidor ASGI de alto rendimiento

---

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva donde puedes probar todos los endpoints directamente desde el navegador:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## Autor

**Mario Losada Enriquez**  
Fecha: 14 de febrero de 2026  
Proyecto: API de Sistema de Reservas - La Mesa Dorada


