from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

# Esquemas de usuarios
from app.schemas.user import (
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate
)

# Servicios de usuarios
from app.services.user_service import (
    get_users,
    update_user_role,
    update_user_status
)

# Solo administradores pueden gestionar usuarios
from app.auth.dependencies import require_roles

# Router para la administración de usuarios
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Lista todos los usuarios registrados (solo administradores)
@router.get(
    "/",
    response_model=list[UserResponse]
)
def read_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin")
    )
):
    return get_users(db)

# Actualiza el rol de un usuario (solo administradores)
@router.patch(
    "/{user_id}/role",
    response_model=UserResponse
)
def change_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin")
    )
):

    # Roles permitidos dentro del sistema
    allowed_roles = [
        "viewer",
        "analyst",
        "admin"
    ]

    # Validar que el rol exista
    if role_data.role not in allowed_roles:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    # Actualizar el rol
    user = update_user_role(
        db,
        user_id,
        role_data.role
    )

    # Si el usuario no existe
    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# Activa o desactiva un usuario (solo administradores)
@router.patch(
    "/{user_id}/status",
    response_model=UserResponse
)
def change_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin")
    )
):

    user = update_user_status(
        db,
        user_id,
        status_data.is_active
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user