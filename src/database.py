import pymongo
# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access a specific database
db = client["shortned_links"]
users_collection = db["user"]

