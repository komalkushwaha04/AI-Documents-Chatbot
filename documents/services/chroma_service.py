import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_document_chunk(chunk, embedding, chunk_id, metadata=None):
    collection.add(
        ids=[chunk_id],
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[metadata or {}]
    )
    
def search_documents(query_embedding, number_of_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    return results