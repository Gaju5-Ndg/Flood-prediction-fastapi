from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

try: 
    mongo_url = os.getenv("MONGO_URL")
    conn = MongoClient(mongo_url)
    
    print("Successfully connected")

except Exception as e:
    print("error on connecting")