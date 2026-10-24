# from django.http import HttpResponse

# from .models import Document
# from .services.pdf_processor import extract_text_from_pdf
# from .services.text_processor import split_text_into_chunks


# def test_pdf_extraction(request):
#     document = Document.objects.first()

#     if not document:
#         return HttpResponse("No document found.")

#     text = extract_text_from_pdf(document.file.path)

#     chunks = split_text_into_chunks(text)

#     output = f"<h1>Total Chunks: {len(chunks)}</h1>"

#     for index, chunk in enumerate(chunks, start=1):
#         output += f"""
#         <h2>Chunk {index}</h2>
#         <pre>{chunk}</pre>
#         <hr>
#         """

#     return HttpResponse(output)
  
from django.http import HttpResponse

from .models import Document
from .services.pdf_processor import extract_text_from_pdf
from .services.vector_store import test_gemini
from .services.embedding_service import generate_embedding
from .services.chroma_service import add_document_chunk
from .services.document_indexer import index_document
from .services.chroma_service import search_documents
from .services.rag_service import ask_document
from django.shortcuts import render
from .services.document_indexer import index_document
from .models import Document


def test_pdf_extraction(request):
    document = Document.objects.first()

    if not document:
        return HttpResponse("No document found.")

    text = extract_text_from_pdf(document.file.path)

    return HttpResponse(
        f"<h1>Extracted Text</h1><pre>{text}</pre>"
    )


def test_gemini_view(request):
    response = test_gemini()

    return HttpResponse(
        f"<h1>Gemini Response</h1><p>{response}</p>"
    )
    
def test_embedding_view(request):
    text = "Django is a Python web framework."

    embedding = generate_embedding(text)

    return HttpResponse(
        f"<h1>Embedding Generated</h1>"
        f"<p>Vector length: {len(embedding)}</p>"
        f"<p>First 5 values: {embedding[:5]}</p>"
    )
    
def test_chroma_view(request):
    text = "Django is a Python web framework."
    
    embedding = generate_embedding(text)

    add_document_chunk(
        chunk=text,
        embedding=embedding,
        chunk_id="test-1"
    )

    return HttpResponse(
        "<h1>ChromaDB Test</h1>"
        "<p>Document chunk successfully stored!</p>"
    )
    
def test_index_document_view(request):
    document = Document.objects.first()

    if not document:
        return HttpResponse("No document found.")

    total_chunks = index_document(document)

    return HttpResponse(
        f"<h1>Document Indexed Successfully</h1>"
        f"<p>Total chunks stored: {total_chunks}</p>"
    )
    
def test_search_view(request):
    question = "What is Django?"

    query_embedding = generate_embedding(question)

    results = search_documents(
        query_embedding=query_embedding,
        number_of_results=3
    )

    documents = results["documents"][0]

    response = "<h1>Search Results</h1>"

    for index, document in enumerate(documents, start=1):
        response += f"<h2>Result {index}</h2>"
        response += f"<p>{document}</p>"

    return HttpResponse(response)
  
  
def test_rag_view(request):
    question = "What is Django?"

    answer = ask_document(question)

    return HttpResponse(
        f"<h1>AI Document Answer</h1>"
        f"<p>{answer}</p>"
    )
    
def chatbot_view(request):

    message = None
    answer = None

    if request.method == "POST":

        # PDF Upload
        if request.FILES.get("pdf_file"):

            pdf_file = request.FILES.get("pdf_file")

            document = Document.objects.create(
                title=pdf_file.name,
                file=pdf_file
            )

            total_chunks = index_document(document)

            message = (
                f"PDF uploaded and indexed successfully! "
                f"{total_chunks} chunks created."
            )

        # Ask Question
        elif request.POST.get("question"):

            question = request.POST.get("question")

            answer = ask_document(question)

    return render(
        request,
        "documents/chatbot.html",
        {
            "message": message,
            "answer": answer,
        }
    )