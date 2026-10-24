from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from documents.views import test_pdf_extraction, test_gemini_view
from documents.views import (
    test_pdf_extraction,
    test_gemini_view,
    test_embedding_view,
    test_chroma_view,
    test_index_document_view,
    test_search_view,
    test_rag_view,
    chatbot_view,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("test-pdf/", test_pdf_extraction),
    path("test-gemini/", test_gemini_view),
    path("test-embedding/", test_embedding_view),
    path("test-chroma/", test_chroma_view),
    path("test-index/", test_index_document_view),
    path("test-search/", test_search_view),
    path("test-rag/", test_rag_view),
    
    path("chatbot/", chatbot_view),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )