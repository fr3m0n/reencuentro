from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Inscrito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    telefono: str
    asistencia: str
    mensaje: Optional[str] = None
    fecha_registro: datetime = Field(default_factory=datetime.now)
    