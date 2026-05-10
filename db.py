from pymongo import MongoClient

MONGO_URI = "mongodb+srv://vskoushal30_db_user:koushal%2B58@cluster0.6zmg3x9.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["lifestyle_db"]

predictions_collection = db["predictions"]