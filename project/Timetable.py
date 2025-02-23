from pymongo import MongoClient
import json  

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["timetable_db"]  # Replace with your DB name
collection = db["timetable"]  # Replace with your collection name

def get_timetable(query):
    """
    Executes the provided query dictionary and retrieves matching timetable documents.
    
    Args:
        query (dict): MongoDB query as a dictionary.
        
    Returns:
        list: List of matching timetable documents or an error message if something goes wrong.
    """
    try:
        if not isinstance(query, dict):
            return "Invalid query format: Query should be a dictionary."

        # Execute the MongoDB query
        results = list(collection.find(query, {"_id": 0}))
        return results if results else "No matching records found."

    except Exception as e:
        return f"Error retrieving timetable: {e}"
