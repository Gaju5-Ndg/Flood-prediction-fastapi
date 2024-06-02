from datetime import datetime
from fastapi import FastAPI, HTTPException
import joblib
import uvicorn
import pandas as pd
from config.db import conn
from fastapi import FastAPI
from models.floodsModel import DataFloods
from schemas.predictionSchema import predictionEntity, predictionsEntity

app = FastAPI()

model = joblib.load('best_model.pkl')

feature_names = ['Water Level (cm)', 'Humidity (%)', 'Temperature (°C)', 'Soil Moisture (%)', 'Timestamp']

def serialize_result(result):
    """
    Helper function to serialize the MongoDB result by converting ObjectId to string.
    """
    if "_id" in result:
        result["_id"] = str(result["_id"])
    if "created_at" in result:
        result["created_at"] = result["created_at"].isoformat()
    return result

@app.post("/floods_detector")
async def floods_detector(data: DataFloods):
    dummy_timestamp = 0 
    features = pd.DataFrame([[data.WaterLevel, data.Humidity, data.Temperature, data.SoilMoisture, dummy_timestamp]], columns=feature_names)
    prediction = model.predict(features)[0]
    prediction_prob = model.predict_proba(features)[0]

    # Interpret the prediction
    if prediction == 0:
        status = "Normal"
    elif prediction == 2:
        status = "Flood"
    elif prediction == 1:
        status = "Drought"
    else:
        status = f"Unexpected class {prediction}"

    result = {
        "water_level": data.WaterLevel,
        "soil_moisture": data.SoilMoisture,
        "humidity": data.Humidity,
        "temperature": data.Temperature,
        "prediction": status,
        "probability": {
            "normal": prediction_prob[0] if len(prediction_prob) > 0 else None,
            "flood": prediction_prob[1] if len(prediction_prob) > 1 else None,
            "drought": prediction_prob[2] if len(prediction_prob) > 2 else None
        },
        "created_at": datetime.now()
    }
    inserted = conn.floods.predictions.insert_one(result)
    inserted_id = str(inserted.inserted_id)
    inserted_result = conn.floods.predictions.find_one({"_id": inserted.inserted_id})
    serialized_result = serialize_result(inserted_result)

    if not inserted_result:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {
        "message": "Data inserted successfully",
        "inserted_id": inserted_id,
        "result": serialized_result
    }
 

@app.get("/read_predictions")
async def get_predictions():
    if conn is None:
        return { "error ": "Database connection not established"}
    
    return predictionsEntity(conn.floods.predictions.find())
    
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)


# floods\Scripts\activate
# uvicorn main:app --reload
