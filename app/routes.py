from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.auth import obtener_usuario_actual
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.get("/", response_model=List[schemas.Tarea])
async def listar_tareas(
    db: AsyncSession = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return await crud.obtener_tareas_por_usuario(db, usuario_actual.id)

@router.get("/{tarea_id}", response_model=schemas.Tarea)
async def obtener_tarea(
    tarea_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    tarea = await crud.obtener_tarea(db, tarea_id)
    if not tarea or tarea.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@router.post("/", response_model=schemas.Tarea)
async def crear_tarea(
    tarea: schemas.TareaCrear,
    db: AsyncSession = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return await crud.crear_tarea(db, tarea, usuario_actual.id)

@router.put("/{tarea_id}", response_model=schemas.Tarea)
async def actualizar_tarea(
    tarea_id: int,
    tarea: schemas.TareaCrear,
    db: AsyncSession = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    tarea_existente = await crud.obtener_tarea(db, tarea_id)
    if not tarea_existente or tarea_existente.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    actualizados = await crud.actualizar_tarea(db, tarea_id, tarea)
    return {**tarea.dict(), "id": tarea_id}

@router.delete("/{tarea_id}")
async def eliminar_tarea(
    tarea_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    tarea_existente = await crud.obtener_tarea(db, tarea_id)
    if not tarea_existente or tarea_existente.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    await crud.eliminar_tarea(db, tarea_id) 
    return {"ok": True, "mensaje": f"Tarea {tarea_id} eliminada"}
