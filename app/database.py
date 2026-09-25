
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[DB_NAME]

# Exact collection names from MongoDB
call_logs = db["call_logs_samples"]
appointments = db["appointment_samples"]
emails = db["emails_sample"]
whatsapp_messages = db["whatsapp_sample"]