from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.user import UserCreate
from app.auth.security import (
    hash_password,
    verify_password
)


# Crea un nuevo usuario en la base de datos
def create_user(db: Session, user: UserCreate):

    # Convertimos la contraseña en un hash antes de almacenarla
    hashed_password = hash_password(user.password)

    # Creamos el objeto User con la información recibida
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="viewer"      # Rol por defecto
    )

    # Agregamos el usuario a la sesión
    db.add(db_user)

    # Guardamos los cambios en PostgreSQL
    db.commit()

    # Refresca el objeto para obtener el ID generado
    db.refresh(db_user)

    # Devolvemos el usuario creado
    return db_user


# Busca un usuario por su nombre de usuario
def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

# Autentica un usuario verificando su contraseña
def authenticate_user(
    db: Session,
    username: str,
    password: str
):

    # Buscar el usuario
    user = get_user_by_username(
        db,
        username
    )

    # Si no existe, autenticación fallida
    if not user:
        return None

    # Comparar la contraseña ingresada con el hash almacenado
    if not verify_password(password,user.hashed_password):
        return None

    # Usuario autenticado correctamente
    return user

# Obtiene todos los usuarios registrados
def get_users(db: Session):

    return db.query(User).all()

# Actualiza el rol de un usuario
def update_user_role(
    db: Session,
    user_id: int,
    role: str
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return None

    user.role = role

    db.commit()

    db.refresh(user)

    return user

# Activar o desactivarun usuario
def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return None

    user.is_active = is_active

    db.commit()

    db.refresh(user)

    return user

# Obtiene un usuario por su nombre de usuario
def get_user_by_username(
    db: Session,
    username: str
):

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )