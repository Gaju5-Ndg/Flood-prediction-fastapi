from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn
import numpy as np



class DataPrediction(BaseModel):
    humidity: float 
    temperature: float 
    soil_moisture: float 
    water_level: float

app = FastAPI()

model = pickle.load(open("linear_regression_model.pkl", "rb"))
@app.get("/")
def index():
    return {"welcome"}

@app.get("/welcome")
def get():
    return {'Welcome To Floods detector'}

@app.post("/floods_detector")
# def floods_detector(data: DataPrediction):
#     prediction = classifier.predict([[data.humidity, data.temperature, data.soil_moisture, data.water_level]])
#     return {"prediction": prediction}
def floods_detector(data: DataPrediction):
    data = data.dict()
    humidity=data['humidity']
    temperature=data['temperature']
    soil_moisture=data['soil_moisture']
    water_level=data['water_level']
    
    prediction = model.predict([[humidity,temperature,soil_moisture,water_level]])
    
    return {"prediction": prediction.tolist()}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=True)
