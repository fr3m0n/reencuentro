from sqlmodel import SQLModel, create_engine
import os

# Esta línea encuentra la carpeta real donde está tu proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(BASE_DIR, "database.db")

# Usamos la ruta segura
engine = create_engine(f"sqlite:///{database_path}")

def crear_db():
    SQLModel.metadata.create_all(engine)