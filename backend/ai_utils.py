# ai_utils.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()
async def generate_book_description(title: str, author: str, genre: str) -> str:
    prompt = (
        f"Write a short, engaging description for a book titled '{title}' by {author} "
        f"in the {genre} genre."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()


async def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']