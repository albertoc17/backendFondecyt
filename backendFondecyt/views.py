from typing import Text
from django.shortcuts import render
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
import mammoth
import json
import os

class FileUploadView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    # tipo_analisis = request.POST['tipo_analisis']
    up_file = request.FILES['file']
    destination = open('backendFondecyt/Docs/' + up_file.name, 'wb+')
    for chunk in up_file.chunks():
      destination.write(chunk)
    destination.close()  # File should be closed only after all chuns are added
    if (up_file.name.split(".")[1] == "docx"):
      with open('backendFondecyt/Docs/' + up_file.name, "rb") as docx_file:
        rawText = mammoth.extract_raw_text(docx_file)
        rawText = rawText.value
        result = mammoth.convert_to_html(docx_file)
        html = result.value
    else:
        txt_file = open('backendFondecyt/Docs/' + up_file.name, "r", encoding="utf-8")
        rawText = txt_file.read()
        txt_file.close()
        txt_file = open('backendFondecyt/Docs/' + up_file.name, "r", encoding="utf-8")
        html = ""
        for line in txt_file:
          stripped_line = line.rstrip()
          if (stripped_line.strip() != ""): 
            html += "<p>" + line + "</p>"
        txt_file.close()
    data = {
      'html': html.encode('utf8'),
      'passive_voice': self.PostRedilegra(rawText, html, "passive_voice"),
      'statistics': self.PostRedilegra(rawText, html, "statistics"),
      'oraciones': self.PostRedilegra(rawText, html, "oraciones"),
      'micro_paragraphs': self.PostRedilegra(rawText, html,  "micro_paragraphs"),
      'gerunds': self.PostRedilegra(rawText, html, "gerunds"),
      'fs_person': self.PostRedilegra(rawText, html, "fs_person"),
      'analisis_concordancia': self.PostRedilegra(rawText, html, "analisis_concordancia"),
      'proposito': self.PostRedilegra(rawText, html, "proposito"),
      'conectores': self.PostRedilegra(rawText, html, "conectores"),
      'sentence_complexity': self.PostRedilegra(rawText, html, "sentence_complexity"),
      'lecturabilidad_parrafo': self.PostRedilegra(rawText, html, "lecturabilidad_parrafo"),
    }
    os.remove('backendFondecyt/Docs/' + up_file.name)
    return Response(data, status.HTTP_201_CREATED)

  def PostRedilegra(self, rawtext, html, endpoint):
    payload = {
      'texto': rawtext,
      'html': html,
    }
    url = 'http://redilegra.com/'+endpoint
    x = requests.post(url, data=payload)
    # print(x.text.encode('utf8'))
    return json.loads(x.text.encode('utf8'))



class SendText(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    html = request.POST['html']
    rawText = request.POST['text']
    data = {
      'html': html.encode('utf8'),
      'passive_voice': self.PostRedilegra(rawText, html, "passive_voice"),
      'statistics': self.PostRedilegra(rawText, html, "statistics"),
      'oraciones': self.PostRedilegra(rawText, html, "oraciones"),
      'micro_paragraphs': self.PostRedilegra(rawText, html,  "micro_paragraphs"),
      'gerunds': self.PostRedilegra(rawText, html, "gerunds"),
      'fs_person': self.PostRedilegra(rawText, html, "fs_person"),
      'analisis_concordancia': self.PostRedilegra(rawText, html, "analisis_concordancia"),
      'proposito': self.PostRedilegra(rawText, html, "proposito"),
      'conectores': self.PostRedilegra(rawText, html, "conectores"),
      'sentence_complexity': self.PostRedilegra(rawText, html, "sentence_complexity"),
      'lecturabilidad_parrafo': self.PostRedilegra(rawText, html, "lecturabilidad_parrafo"),
    }
    return Response(data, status.HTTP_201_CREATED)

  def PostRedilegra(self, rawtext, html, endpoint):
    payload = {'texto': rawtext, 'html': html}
    url = 'http://redilegra.com/'+endpoint
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))



class Proposito(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    html = request.POST['html']
    text = request.POST['text']
    macromovida = request.POST['macromovida']
    data = {'proposito': self.PostRedilegra(text, html, "proposito", macromovida)}
    return Response(data, status.HTTP_201_CREATED)

  def PostRedilegra(self, rawtext, html, endpoint, macromovida):
    payload = {'texto': rawtext, 'html': html, 'proposito': macromovida}
    url = 'http://redilegra.com/'+endpoint
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))



class Concordancia(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    patron = request.POST['patron']
    modelo = request.POST['modelo']
    data = self.PostConcordancia(patron, modelo)
    return Response(data, status.HTTP_201_CREATED)

  def PostConcordancia(self, patron, modelo):
    payload = {'patron': patron, 'modelo': modelo}
    url = 'http://redilegra.com/Concordancia'
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))