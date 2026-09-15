import os
from dotenv import load_dotenv
import requests
from google import genai

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
}

r = requests.get(
    "https://models.github.ai/catalog/models",
    headers=headers
)

models = r.json()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

for model in client.models.list():
    print(model.name, model.description)

for model in models:
    print(model["name"], model["description"])