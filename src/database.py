import pymongo
from dotenv import load_dotenv
from os import getenv

# Connect to MongoDB
load_dotenv()
MONGODB_SERVER_IP = getenv("MONGODB_SERVER_IP")
client = pymongo.MongoClient(f"mongodb://{MONGODB_SERVER_IP}/")

# Access a specific database
db = client["shortned_links"]
users_collection = db["user"]
link_collection = db["link"]
