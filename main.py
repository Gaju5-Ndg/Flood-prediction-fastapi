from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
import uvicorn
import numpy as np
# from motor.motor_asyncio import AsyncIOMotorClient


class DataPrediction(BaseModel):
    TopographyDrainage: float
    RiverManagement: float
    Deforestation: float
    Urbanization: float
    ClimateChange: float

app = FastAPI()

model = joblib.load('linear_regression_model.pkl')

@app.get("/floods_data/")
async def get_floods_data(
    topography_drainage: float = Query(..., description="Topography and drainage value"),
    river_management: float = Query(..., description="River management value"),
    deforestation: float = Query(..., description="Deforestation value"),
    urbanization: float = Query(..., description="Urbanization value"),
    climate_change: float = Query(..., description="Climate change value"),
):
    # Prepare the input features
    features = np.array([[topography_drainage, river_management, deforestation, urbanization, climate_change]])
    prediction = model.predict(features)
    prediction_list = prediction.tolist()
    return {"prediction": prediction_list}

# @app.get("/")
# def index():
#     return {"welcome"}

# @app.get("/welcome")
# def get():
#     return {'Welcome To Floods detector'}

@app.post("/floods_detector")
async def floods_detector(data: DataPrediction):
    features = np.array([[data.TopographyDrainage, data.RiverManagement, data.Deforestation,
                          data.Urbanization, data.ClimateChange]])
    prediction = model.predict(features)
    prediction_list = prediction.tolist()       
    return {"prediction": prediction_list}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# floods\Scripts\activate
#uvicorn main:app --reload