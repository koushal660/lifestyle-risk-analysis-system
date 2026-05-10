from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://vskoushal30_db_user:koushal%2B58@cluster0.6zmg3x9.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["lifestyle_db"]

predictions_collection = db["predictions"]