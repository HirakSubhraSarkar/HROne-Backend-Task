from pymongo import MongoClient, ReturnDocument

# Connect to MongoDB
client = MongoClient("mongodb+srv://hiraksubhrasarkat:qW1z9JLSFAms1FRK@cluster0.egtxsz2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select database
db = client["HROne"]

# Collections
collection = db["products"]
orders_collection = db["orders"]


counters = db["counters"]

# Initialize counter if not exists
if counters.count_documents({"_id": "id"}) == 0:
    counters.insert_one({"_id": "id", "sequence_value": 12344})
    print("✅ Counter initialized with sequence_value = 12344")

# Helper to get next id
def get_next_id():
    ret = counters.find_one_and_update(
        {"_id": "id"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return ret["sequence_value"]
