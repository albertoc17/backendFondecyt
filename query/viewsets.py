from rest_framework import viewsets

from .models import Book, QueryApi
from .serializer import BookSerializer, QueryApiSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class QueryApiViewSet(viewsets.ModelViewSet):
    queryset = QueryApi.objects.all()
    serializer_class = QueryApiSerializer