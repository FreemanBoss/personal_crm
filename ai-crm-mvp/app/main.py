from crm_logic import generate_linkedin_url, generate_message
from fastapi import FastAPI, UploadFile, File
from utils import extract_text_from_image, extract_contacts
import shutil
import os

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)  # Ensure 'data/' exists

    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text_lines = extract_text_from_image(file_path)
    contacts = extract_contacts(text_lines)

    enriched_contacts = []
    for person in contacts:
        name = person.get("name", "")
        org = "MIT"  # You can replace this dynamically
        linkedin_url = generate_linkedin_url(name, org)
        message = generate_message(name)
        enriched_contacts.append({
            "name": name,
            "organization": org,
            "linkedin_url": linkedin_url,
            "message": message
        })

    return {
        "contacts": enriched_contacts,
        "raw_text": text_lines
    }
