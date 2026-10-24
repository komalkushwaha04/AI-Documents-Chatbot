# import chromadb


# client = chromadb.PersistentClient(path="chroma_db")

# collection = client.get_or_create_collection(
#     name="documents"
# )
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def test_gemini():
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Explain Django in one sentence."
    )

    return response.text