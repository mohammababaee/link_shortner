import pymongo
from dotenv import load_dotenv
from os import getenv

# Connect to MongoDB
load_dotenv()
MONGODB_SERVER_IP = getenv("MONGODB_SERVER_IP")
MONGODB_USERNAME = getenv("MONGO_INITDB_ROOT_USERNAME")
MONGODB_PASSWORD = getenv("MONGO_INITDB_ROOT_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER_IP}/"
)

# Access a specific database
db = client["shortned_links"]
users_collection = db["user"]
link_collection = db["link"]
