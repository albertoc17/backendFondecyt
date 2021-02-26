from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QueryApi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    consulta = models.TextField()
    tipo = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()