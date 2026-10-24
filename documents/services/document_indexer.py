from .pdf_processor import extract_text_from_pdf
from .text_processor import split_text_into_chunks
from .embedding_service import generate_embedding
from .chroma_service import add_document_chunk


def index_document(document):
    text = extract_text_from_pdf(document.file.path)

    chunks = split_text_into_chunks(text)

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        chunk_id = f"document-{document.id}-chunk-{index}"

        add_document_chunk(
            chunk=chunk,
            embedding=embedding,
            chunk_id=chunk_id,
            metadata={
                "document_id": document.id,
                "filename": document.title,
            }
        )

    return len(chunks)