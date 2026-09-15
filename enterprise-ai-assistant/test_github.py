import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()

""""client = ChatCompletionsClient(
    endpoint="https://models.github.ai/inference",
    credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
)"""

"""client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)"""

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

"""response = client.complete(
    model="openai/gpt-4.1",
    messages=[
        UserMessage(content="Say hello in one sentence.")
    ],
)"""
"""response = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ]
)"""
response = client.models.generate_content(
    model="models/gemini-3.6-flash",
    contents="Say hello in one sentence."
)

print(response.text)