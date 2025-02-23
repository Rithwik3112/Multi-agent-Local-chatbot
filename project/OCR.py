import google.generativeai as genai
import PIL.Image
from pymongo import MongoClient
import json
import re

# Configure Gemini API
genai.configure(api_key="AIzaSyBrebjwXquFDImuNrDqBjl6pw-n_Q5VhbU")

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["timetable_db"]
collection = db["timetable"]

def add_timetable_to_db(image_path):
    """
    Extracts timetable from the image and stores it in MongoDB.
    Removes old data before inserting new tasks.
    
    Args:
        image_path (str): Path to the timetable image.
        
    Returns:
        str: Success or error message.
    """
    try:
        image = PIL.Image.open(image_path)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content([
            "Extract the timetable in strict JSON format (no extra text). Each task should be an object with fields: "
            "'day', 'start_time', 'end_time', 'class', 'instructor', 'location'. Wrap all tasks in an array []. "
            "Ensure there is no extra explanation or formatting.",
            image
        ])

        response_text = response.text.strip()

        # Extract JSON using regex in case extra text is included
        match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if match:
            json_string = match.group(0)
        else:
            return "Error: No valid JSON found in response."

        timetable_data = json.loads(json_string)

        if not isinstance(timetable_data, list):
            return "Error: Extracted JSON is not a list of tasks."

        collection.delete_many({})  # Clear old data
        collection.insert_many(timetable_data)  # Insert new data

        return "Timetable successfully added to the database."

    except Exception as e:
        return f"Error processing timetable: {e}"
    
add_timetable_to_db("time_table.jpg")  