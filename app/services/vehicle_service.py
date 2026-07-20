from sqlalchemy.orm import Session
from app.database.models import Vehicle
from app.schemas.vehicle import VehicleCreate

def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(
        plate=vehicle.plate,
        brand=vehicle.brand,
        model=vehicle.model,
        year=vehicle.year
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles(db: Session):
    return db.query(Vehicle).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

def update_vehicle(db: Session, vehicle_id: int, vehicle: VehicleCreate):
    db_vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not db_vehicle:
        return None

    db_vehicle.plate = vehicle.plate
    db_vehicle.brand = vehicle.brand
    db_vehicle.model = vehicle.model
    db_vehicle.year = vehicle.year

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not db_vehicle:
        return None

    db.delete(db_vehicle)
    db.commit()

    return db_vehicle