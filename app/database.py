from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Definimos la ruta donde se creará el archivo .db
# "./app/data/" asegura que se guarde en tu carpeta data
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/data/restaurante.db"

# Crear el motor (Engine)
# check_same_thread=False es necesario solo en SQLite para evitar errores con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la fábrica de sesiones (SessionLocal)
# Cada vez que un usuario haga una petición, usaremos esto para crear una "conexión" temporal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la Base
# De esta clase heredarán tus modelos (ClienteDB, MesaDB, ReservaDB)
Base = declarative_base()

# Dependencia
# Esta función se usará en los Routers para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()