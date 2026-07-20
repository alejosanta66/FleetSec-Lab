from pydantic import BaseModel


class VehicleCreate(BaseModel):
    plate: str
    brand: str
    model: str
    year: int

class VehicleResponse(BaseModel):
    id: int
    plate: str
    brand: str
    model: str
    year: int

    class Config:
        from_attributes = True