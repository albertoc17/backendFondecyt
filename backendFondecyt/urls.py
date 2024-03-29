"""backendFondecyt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backendFondecyt import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/',include('query.urls')),
    path('api/FileUploadView', views.FileUploadView.as_view()),
    path('api/Concordancia', views.Concordancia.as_view()),
    path('api/Conceptualizacion', views.Conceptualizacion.as_view()),
    path('api/Ideacion', views.Ideacion.as_view()),
    path('api/Transcripcion', views.Transcripcion.as_view()),
    path('api/Reconceptualizacion', views.Reconceptualizacion.as_view()),
    path('api/SendText', views.SendText.as_view()),
    path('api/SendText2', views.SendText2.as_view()),
    path('api/Proposito', views.Proposito.as_view())
]