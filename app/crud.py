from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Tarea
from app import schemas

async def obtener_tareas_por_usuario(db: AsyncSession, usuario_id: int):
    result = await db.execute(select(Tarea).where(Tarea.usuario_id == usuario_id))
    return result.scalars().all()

async def obtener_tarea(db: AsyncSession, tarea_id: int):
    result = await db.execute(select(Tarea).where(Tarea.id == tarea_id))
    return result.scalar_one_or_none()

async def crear_tarea(db: AsyncSession, tarea: schemas.TareaCrear, usuario_id: int):
    nueva = Tarea(**tarea.model_dump(), usuario_id=usuario_id)
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def actualizar_tarea(db: AsyncSession, tarea_id: int, tarea: schemas.TareaCrear):
    result = await db.execute(select(Tarea).where(Tarea.id == tarea_id))
    tarea_existente = result.scalar_one_or_none()
    if not tarea_existente:
        return 0
    tarea_existente.titulo = tarea.titulo
    tarea_existente.descripcion = tarea.descripcion
    tarea_existente.completado = tarea.completado
    await db.commit()
    return 1

async def eliminar_tarea(db: AsyncSession, tarea_id: int):
    result = await db.execute(select(Tarea).where(Tarea.id == tarea_id))
    tarea = result.scalar_one_or_none()
    if tarea:
        await db.delete(tarea)
        await db.commit()
        return 1
    return 0