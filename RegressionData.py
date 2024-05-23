from pydantic import BaseModel

class DataPrediction(BaseModel):
    WaterLevel: float
    SoilMoisture: float
    Humidity: float
    Temperature: float
    
