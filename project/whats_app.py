import pywhatkit
import csv

# Function to load contacts from CSV into a dictionary
def load_contacts(csv_filename):
    contacts = {}
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts[row['Name'].strip().lower()] = row['PhoneNumber'].strip()  # Convert name to lowercase for consistency
    return contacts

# Function to send WhatsApp message
def send_whatsapp_message(contact_name, message):
    csv_filename='contacts.csv'
    contacts = load_contacts(csv_filename)
    contact_number = contacts.get(contact_name.lower())  # Case insensitive match
    if contact_number:
        pywhatkit.sendwhatmsg_instantly(contact_number, message, wait_time=10)
        return f"Message sent to {contact_name} ({contact_number})."
    else:
        return f"Contact '{contact_name}' not found in {csv_filename}."

# Example Usage
