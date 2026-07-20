from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
from sqlalchemy.orm import Session

from app.auth.jwt_handler import verify_access_token
from app.database.database import get_db
from app.services.user_service import get_user_by_username
from app.database.models import User

# Swagger utilizará este endpoint para solicitar el JWT
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# Obtiene la información del usuario autenticado
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # 1. Valida el JWT recibido
    payload = verify_access_token(token)

    # 2. Si el token es inválido o expiró, frena de inmediato aquí
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 3. Obtener el nombre de usuario almacenado en el JWT
    username = payload.get("sub")

    # Programación defensiva por si el token no trae el campo "sub"
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # 4. Buscar el usuario en la base de datos
    user = get_user_by_username(db, username)

    # 5. Validar que el usuario exista y esté activo
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or does not exist",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Devuelve el objeto User de la base de datos
    return user


# Verifica si el usuario posee alguno de los roles permitidos
def require_roles(*allowed_roles: str) -> Callable:

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        user_role = current_user.role

        # Si el rol no está autorizado
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )

        # Retornar la información del usuario autenticado
        return current_user

    return role_checker