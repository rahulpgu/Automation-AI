from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
question = input("Ask a question: ")
response = client.responses.create(
    model="gpt-5",
    input=question
)
print("Response from GPT-5:")
print(response.output_text)