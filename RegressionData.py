from pydantic import BaseModel

class DataPrediction(BaseModel):
    humidity: float 
    temperature: float 
    soil_moisture: float 
    water_level: float
