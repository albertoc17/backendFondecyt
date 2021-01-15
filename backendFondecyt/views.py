from django.shortcuts import render
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
import requests
import mammoth

class FileUploadView(APIView):
    parser_classes = ( MultiPartParser, FormParser)

    def post(self, request, format=None):
        up_file = request.FILES['file']
        destination = open('backendFondecyt/Docs/word.docx', 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()  # File should be closed only after all chuns are added
        
        with open('backendFondecyt/Docs/word.docx', "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            rawText = mammoth.extract_raw_text(docx_file)
            html = result.value # The generated HTML
            
            f = open("backendFondecyt/Docs/output.html", "wb")
            f.write(html.encode('utf8'))
            f.close()
            a = { 'html' : html.encode('utf8'),
                'passive_voice': self.PostRedilegra(rawText, "passive_voice"),
                'statistics': self.PostRedilegra(rawText, "statistics")
            }
        return Response(a   , status.HTTP_201_CREATED)

    def PostRedilegra(self, rawtext, function):
        payload = { 'texto' : rawtext,
                 'funcion': function }
        url = 'http://redilegra.com/palabra'
        x = requests.post(url, data=payload)
        return x.text.encode('utf8')
