from pydantic import BaseModel

class DataPrediction(BaseModel):
    TopographyDrainage: float
    RiverManagement: float
    Deforestation: float
    Urbanization: float
    ClimateChange: float
