import time

from .embedding_service import generate_embedding
from .chroma_service import search_documents
from .vector_store import client


def ask_document(question):

    # 1. Convert question into embedding
    query_embedding = generate_embedding(question)

    # 2. Search ChromaDB
    results = search_documents(
        query_embedding=query_embedding,
        number_of_results=3
    )

    # 3. Get relevant PDF chunks
    documents = results["documents"][0]
    chunk_ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    
    # 4. Display the source PDFs in the terminal
    print("\n--- RETRIEVED SOURCES ---")

    for chunk_id, metadata in zip(chunk_ids, metadatas):
        print("Chunk ID:", chunk_id)
        print("Source PDF:", (metadata or {}).get("filename", "Unknown"))
        print("-" * 40)

    # 5. Build context
    context = "\n\n".join(documents)

    # 6. Create prompt
    prompt = f"""
You are an AI assistant that answers questions using the provided document.

Use ONLY the information from the document context below.

If the answer is not available in the document, say:
"I could not find the answer in the document."

Document context:
{context}

Question:
{question}

Answer:
"""

    # 7. Ask Gemini with retry
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as error:
            print(
                f"Gemini attempt {attempt + 1} failed: {error}"
            )

            if attempt == 2:
                return (
                    "Gemini is temporarily unavailable. "
                    "Please try again in a few moments."
                )

            time.sleep(5 * (2 ** attempt))
            
            