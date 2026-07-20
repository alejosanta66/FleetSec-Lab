from pathlib import Path
import sys

# Forzamos a Python a buscar primero en la raíz del proyecto
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.database.database import SessionLocal
from app.database.models import User
from app.auth.security import hash_password


# Crea un usuario administrador inicial o lo repara si ya existe
def seed_admin():

    db = SessionLocal()

    try:

        # Buscar si ya existe un usuario administrador
        admin = (
            db.query(User)
            .filter(User.username == "admin")
            .first()
        )

        if admin:
            # Si ya existe, forzamos que tenga el rol correcto y esté activo
            admin.role = "admin"
            admin.is_active = True
            
            db.commit()
            print("✔ Usuario administrador actualizado.")
            return

        # Crear el administrador inicial si no existe
        admin = User(
            username="admin",
            email="admin@fleetsec.local",
            hashed_password=hash_password("Admin123*"),
            role="admin",
            is_active=True
        )

        db.add(admin)

        db.commit()

        db.refresh(admin)

        print("✔ Usuario administrador creado correctamente.")

    except Exception as e:

        db.rollback()

        print(f"❌ Error: {e}")

    finally:

        db.close()


# Punto de entrada del script
if __name__ == "__main__":

    seed_admin()