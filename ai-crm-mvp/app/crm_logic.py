from openai import OpenAI
import os
import re
import requests


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "your-serpapi-key-here")


def generate_linkedin_url(name: str, org: str = ""):
    # Clean name and organization
    clean_name = re.sub(r"[^a-zA-Z0-9 ]", "", name).strip().lower()
    clean_org = re.sub(r"[^a-zA-Z0-9 ]", "", org).strip().lower()

    formatted_name = "-".join(clean_name.split())  # use hyphens
    formatted_org = "-".join(clean_org.split())

    return f"https://www.linkedin.com/in/{formatted_name}-{formatted_org}"

def generate_message(name: str, context: str = "MIT AI Global Hackathon"):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Write a short, friendly LinkedIn connection message to {name}, whom I met at the {context}. Keep it professional and warm."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating message: {e}"


def search_linkedin_profile(name: str, org: str = "") -> str:
    try:
        query = f"{name} {org} site:linkedin.com/in"
        url = "https://serpapi.com/search.json"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 1
        }
        response = requests.get(url, params=params)
        results = response.json().get("organic_results", [])
        if results and "link" in results[0]:
            return results[0]["link"]
    except Exception as e:
        print("Search error:", e)
    return "https://www.linkedin.com"
