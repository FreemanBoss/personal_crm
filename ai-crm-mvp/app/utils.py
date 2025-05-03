import re


def extract_text_from_image(image_path):
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)
    text_lines = [item[1] for item in results]
    return text_lines

def extract_contacts(text_lines):
    contacts = []
    for line in text_lines:
        if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', line):  # crude name pattern
            contacts.append({'name': line})
    return contacts


# text_lines = extract_text_from_image("data/sample_card.jpg")
# contacts = extract_contacts(text_lines)
# print(contacts)
