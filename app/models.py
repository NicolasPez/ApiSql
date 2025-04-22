from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import DateTime, func

Base = declarative_base()

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    completado = Column(Boolean, default=False)
    
    # Relación con la tabla Usuario
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Enlace a Usuario
    usuario = relationship("Usuario", back_populates="tareas")  # Relación inversa

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    creado_en = Column(DateTime, server_default=func.now())

    # Relación inversa con Tarea
    tareas = relationship("Tarea", back_populates="usuario")