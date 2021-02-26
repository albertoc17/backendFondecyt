from .models import Book, QueryApi
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class QueryApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryApi
        fields = '__all__'