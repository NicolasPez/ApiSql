from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import router as tareas_router
from app.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Tareas API",
    swagger_ui_init_oauth={
        "clientId": "swagger-ui",
        "scopes": ["openid"],
        "usePkceWithAuthorizationCodeGrant": True
    }
)

app.include_router(auth_router)
app.include_router(tareas_router) 
