from pydantic import BaseModel

class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    completado: bool
    
    class Config:
        orm_mode = True

class TareaCrear(TareaBase):
    pass  # Se usa cuando se crea una tarea, no necesita ID

class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True
        
class UsuarioCrear(BaseModel):
    email: str
    password: str

class Usuario(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str  