from pydantic import BaseModel
from datetime import datetime

class DataFloods(BaseModel):
    WaterLevel: float
    SoilMoisture: float
    Humidity: float
    Temperature: float
    created_at: datetime = datetime.now()
    