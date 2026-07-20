from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import require_roles
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle_service import (
    create_vehicle,
    get_vehicles,
    get_vehicle,
    update_vehicle,
    delete_vehicle
)
# Mensaje reutilizable para respuestas y solucion del primer error encontrado por sonarquebe
VEHICLE_NOT_FOUND = "Vehicle not found"

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

# 1. Crear vehículo
@router.post(
        "/", 
        response_model=VehicleResponse
)
def create(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles(
            "analyst","admin"
             )
    )
):
    return create_vehicle(db, vehicle)

# 2. Obtener todos los vehículos (requiere autenticación)
@router.get(
        "/", 
        response_model=list[VehicleResponse]
)
def read_vehicles(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles(
            "viewer", "analyst", "admin"
              )   
    )               
):
    return get_vehicles(db)

# 3. Obtener un vehículo por ID
@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def read_vehicle_by_id(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles(
            "viewer",
            "analyst",
            "admin"
        )
    )
):
    vehicle = get_vehicle(
        db,
        vehicle_id
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail=VEHICLE_NOT_FOUND
        )

    return vehicle

# 4. Editar un vehículo por ID
@router.put(
        "/{vehicle_id}", 
        response_model=VehicleResponse
)
def edit_vehicle(
    vehicle_id: int,
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin"))
):
    updated_vehicle = update_vehicle(
        db,
        vehicle_id,
        vehicle
    )
    
    if not updated_vehicle:
        raise HTTPException(
            status_code=404,
            detail=VEHICLE_NOT_FOUND
        )
        
    return updated_vehicle

# 5. Eliminar un vehículo por ID
@router.delete(
        "/{vehicle_id}", 
        response_model=VehicleResponse
)
def remove_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin"))
):
    deleted_vehicle = delete_vehicle(db, vehicle_id)
    
    if not deleted_vehicle:
        raise HTTPException(
            status_code=404,
            detail=VEHICLE_NOT_FOUND
        )
        
    return deleted_vehicle
