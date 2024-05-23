def predictionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "water_level": item["water_level"],  # Adjusted key to lowercase 'l'
        "soil_moisture": item["soil_moisture"],
        "humidity": item["humidity"],
        "prediction":item["prediction"],
        "temperature": item["temperature"],
        "created_at": item["created_at"]
    }
def predictionsEntity(entity) -> list:
    return [predictionEntity(item) for item in entity]