from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn
import numpy as np


class DataPrediction(BaseModel):
    TopographyDrainage: float
    RiverManagement: float
    Deforestation: float
    Urbanization: float
    ClimateChange: float

app = FastAPI()

model = joblib.load('linear_regression_model.pkl')

@app.get("/")
def index():
    return {"welcome"}

@app.get("/welcome")
def get():
    return {'Welcome To Floods detector'}

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