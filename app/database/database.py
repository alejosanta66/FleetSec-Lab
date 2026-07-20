from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


# prueba de conexión a la base de datos
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("=" * 60)
        print("✅ Conexión exitosa con PostgreSQL")
        print(result.scalar())
        print("=" * 60)

except Exception as e:
    print("=" * 60)
    print("❌ Error de conexión")
    print(e)
    print("=" * 60)

#crea una dependencia para FastAPI y la conexion al terminar la cierra

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()