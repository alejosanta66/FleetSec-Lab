from datetime import datetime
from pydantic import BaseModel, EmailStr

# Datos requeridos para registrar un usuario nuevo
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Datos públicos que devuelve la API (excluye la contraseña por seguridad)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

# Permite mapear directamente objetos de SQLAlchemy (ORM)
    class Config:
        from_attributes = True

# Datos requeridos para el inicio de sesión
class UserLogin(BaseModel):
    username: str
    password: str
    
# Permite actualizar únicamente el rol de un usuario
class UserRoleUpdate(BaseModel):
    role: str


# Permite activar o desactivar un usuario
class UserStatusUpdate(BaseModel):
    is_active: bool    