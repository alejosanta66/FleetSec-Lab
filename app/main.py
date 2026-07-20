from fastapi import FastAPI
from app.database.database import engine
from app.database.base import Base
import app.database.models

# Importación de controladores (Routers)
from app.routes.vehicle_routes import router as vehicle_router
from app.routes.user_routes import router as user_router
from app.auth.auth_route import router as auth_router

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="FleetSec API",
    description="DevSecOps Security Laboratory",
    version="1.0.0"
)

# Creación automática de tablas en la base de datos al arrancar
Base.metadata.create_all(bind=engine)

# Registro de rutas globales en la aplicación
app.include_router(vehicle_router)
app.include_router(auth_router)
app.include_router(user_router)

# Endpoint base de verificación
@app.get("/")
async def root():
    return {
        "application": "FleetSec API",
        "status": "online",
        "version": "1.0.0"
    }

# Endpoint de diagnóstico
@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
