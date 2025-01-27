from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    store=True,
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)
