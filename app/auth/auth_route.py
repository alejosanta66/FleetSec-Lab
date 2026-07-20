from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

# Router para todos los endpoints relacionados con autenticación
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Registro de nuevos usuarios
@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)

# Inicio de sesión
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Verificar usuario y contraseña
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    # Credenciales inválidas
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Crear el JWT
    access_token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    # Devolver el token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }