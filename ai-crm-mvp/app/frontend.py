import streamlit as st
import pandas as pd
import json
import tempfile
from io import StringIO
from pathlib import Path

from utils import extract_text_from_image, extract_contacts
from crm_logic import generate_linkedin_url, generate_message

# Constants
MEMORY_FILE = Path("crm_memory.json")


# ----------------------
# Utility Functions
# ----------------------

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_memory(entry):
    memory = load_memory()
    memory.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# ----------------------
# Streamlit App
# ----------------------

st.set_page_config(page_title="Personal CRM Assistant", layout="wide")
st.title("🤖 Personal CRM Assistant")

# --- Upload Section ---
st.header("1. Upload Contact Source (Image)")
uploaded_file = st.file_uploader("Upload image (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(uploaded_file.read())
        file_path = temp.name

    st.success("✅ File uploaded!")

    # Step 1: Extract text and names
    text_lines = extract_text_from_image(file_path)
    contacts = extract_contacts(text_lines)

    st.subheader("📋 Extracted Contacts")
    if not contacts:
        st.warning("No valid names found. Try a different image.")
    else:
        for contact in contacts:
            name = contact.get("name", "Unknown")

            # Try to guess organization from lines near the name
            name_index = next((i for i, line in enumerate(text_lines) if name.lower() in line.lower()), None)
            org_guess = "Independent"
            if name_index is not None:
                nearby_lines = text_lines[name_index+1:name_index+4]
                org_guess = next((line for line in nearby_lines if line.strip()), "Independent")

            # Build full contact object
            linkedin_url = generate_linkedin_url(name, org_guess)
            message = generate_message(name)

            profile = {
                "full_name": name,
                "headline": f"{org_guess}",
                "organization": org_guess,
                "linkedin_url": linkedin_url,
                "personalized_message": message
            }

            save_to_memory(profile)

            with st.expander(name):
                st.markdown(f"**Organization:** {org_guess}")
                st.markdown(f"[LinkedIn Profile]({linkedin_url})")
                st.markdown(f"**Message:**\n> {message}")

    st.subheader("📄 Raw Text from Image")
    st.code("\n".join(text_lines))


# --- Memory & Search Section ---
st.header("2. Saved Contacts (Searchable Memory)")
crm_data = load_memory()

search_query = st.text_input("Search contacts by name, organization, or title")

if search_query:
    filtered = [
        c for c in crm_data
        if search_query.lower() in c['full_name'].lower()
        or search_query.lower() in c['organization'].lower()
        or search_query.lower() in c['headline'].lower()
    ]
else:
    filtered = crm_data

if filtered:
    for contact in filtered:
        st.subheader(contact['full_name'])
        st.write(f"**Title / Headline:** {contact['headline']}")
        st.write(f"**Organization:** {contact['organization']}")
        st.markdown(f"[LinkedIn Profile]({contact['linkedin_url']})")
        st.markdown(f"**Message:** {contact['personalized_message']}")
        st.markdown("---")
else:
    st.info("No contacts found for your search.")

# --- Export Section ---
if crm_data:
    st.subheader("📤 Export Your CRM")
    df = pd.DataFrame(crm_data)

    # CSV Download
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("⬇️ Download CSV", data=csv_buffer.getvalue(), file_name="crm_memory.csv", mime="text/csv")

    # JSON Download
    st.download_button("⬇️ Download JSON", data=json.dumps(crm_data, indent=2), file_name="crm_memory.json", mime="application/json")
