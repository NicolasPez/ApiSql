from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import models
from sqlalchemy import select
from fastapi import APIRouter
from app import schemas
from fastapi.security import HTTPAuthorizationCredentials

# Configuraciones
SECRET_KEY = "secret-key-super-segura"  # Cambiá esto por una key real en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer(auto_error=False)

# Funciones de hash
def verificar_contraseña(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashear_contraseña(password):
    return pwd_context.hash(password)

# Crear token JWT
def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Obtener usuario desde token
async def obtener_usuario_actual(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_invalidas
    except JWTError:
        raise credenciales_invalidas

    result = await db.execute(select(models.Usuario).where(models.Usuario.email == email))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise credenciales_invalidas
    return usuario

router = APIRouter(tags=["Autenticación"])

# Registro
@router.post("/registro", response_model=schemas.Usuario)
async def registrar_usuario(usuario: schemas.UsuarioCrear, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Usuario).where(models.Usuario.email == usuario.email))
    usuario_existente = result.scalar_one_or_none()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = hashear_contraseña(usuario.password)
    nuevo_usuario = models.Usuario(email=usuario.email, hashed_password=hashed_password)
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

# Login
@router.post("/login", response_model=schemas.Token)
async def login(usuario: schemas.UsuarioCrear, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Usuario).where(models.Usuario.email == usuario.email))
    db_usuario = result.scalar_one_or_none()
    if not db_usuario or not verificar_contraseña(usuario.password, db_usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = crear_token(data={"sub": db_usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}