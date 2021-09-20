from typing import Text
from django.shortcuts import render
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
import requests
import mammoth
import os
import subprocess

class FileUploadView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    # tipo_analisis = request.POST['tipo_analisis']
    uploaded_file = request.FILES['file']
    file_name = uploaded_file.name
    file_extension = file_name.split(".")[1]

    destination = open('backendFondecyt/Docs/' + file_name, 'wb+')
    for chunk in uploaded_file.chunks():
      destination.write(chunk)
    destination.close()

    if (file_extension == "doc"):
      file_name = self.converDocToDocx(file_name)
    if (file_extension == "doc" or file_extension == "docx"):
      with open('backendFondecyt/Docs/' + file_name, "rb") as docx_file:
        rawText = mammoth.extract_raw_text(docx_file)
        rawText = rawText.value
        result = mammoth.convert_to_html(docx_file)
        html = result.value
    if (file_extension == "txt"):
        txt_file = open('backendFondecyt/Docs/' + file_name, "r", encoding="utf-8")
        rawText = txt_file.read()
        txt_file.close()
        txt_file = open('backendFondecyt/Docs/' + file_name, "r", encoding="utf-8")
        html = ""
        for line in txt_file:
          stripped_line = line.rstrip()
          if (stripped_line.strip() != ""): 
            html += "<p>" + line + "</p>"
        txt_file.close()
    data = {
      'html': html.encode('utf8'),
      'passive_voice': self.postAnalisis(rawText, html, "passive_voice"),
      'statistics': self.postAnalisis(rawText, html, "statistics"),
      'oraciones': self.postAnalisis(rawText, html, "oraciones"),
      'micro_paragraphs': self.postAnalisis(rawText, html,  "micro_paragraphs"),
      'gerunds': self.postAnalisis(rawText, html, "gerunds"),
      'fs_person': self.postAnalisis(rawText, html, "fs_person"),
      'analisis_concordancia': self.postAnalisis(rawText, html, "analisis_concordancia"),
      'proposito': self.postAnalisis(rawText, html, "proposito"),
      'conectores': self.postAnalisis(rawText, html, "conectores"),
      'sentence_complexity': self.postAnalisis(rawText, html, "sentence_complexity"),
      'lecturabilidad_parrafo': self.postAnalisis(rawText, html, "lecturabilidad_parrafo"),
    }
    os.remove('backendFondecyt/Docs/' + file_name)
    return Response(data, status.HTTP_201_CREATED)

  def postAnalisis(self, rawtext, html, endpoint):
    payload = {
      'texto': rawtext,
      'html': html,
    }
    url = 'http://redilegra.com/'+endpoint
    x = requests.post(url, data=payload)
    # print(x.text.encode('utf8'))
    return json.loads(x.text.encode('utf8'))

  def converDocToDocx(self, file_name):
    lowriter = 'libreoffice'
    outdir = './backendFondecyt/Docs'
    file_path = './backendFondecyt/Docs/' + file_name
    subprocess.run('"{}" --convert-to docx --outdir "{}" "{}"'.format(lowriter, outdir, file_path), shell=True)
    os.remove('./backendFondecyt/Docs/' + file_name)
    new_docx_file_name = file_name + "x"
    return new_docx_file_name


class SendText(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    html = request.POST['html']
    rawText = request.POST['text']
    data = {
      'html': html.encode('utf8'),
      'statistics': self.postAnalisis(rawText, html, "statistics"),
      'gerunds': self.postAnalisis(rawText, html, "gerunds"),
      'oraciones': self.postAnalisis(rawText, html, "oraciones"),
      'micro_paragraphs': self.postAnalisis(rawText, html,  "micro_paragraphs"),
      'fs_person': self.postAnalisis(rawText, html, "fs_person"),
      'passive_voice': self.postAnalisis(rawText, html, "passive_voice"),
      'conectores': self.postAnalisis(rawText, html, "conectores"),
      'conectores2': self.postAnalisis(rawText, html, "conectores2"),
      'sentence_complexity': self.postAnalisis(rawText, html, "sentence_complexity"),
      'lecturabilidad_parrafo': self.postAnalisis(rawText, html, "lecturabilidad_parrafo"),
      'proposito': self.postAnalisis(rawText, html, "proposito")
      # 'analisis_concordancia': self.postAnalisis(rawText, html, "analisis_concordancia"),
    }
    return Response(data, status.HTTP_201_CREATED)

  def postAnalisis(self, rawtext, html, endpoint):
    payload = {'texto': rawtext, 'html': html}
    url = 'http://redilegra.com/'+endpoint
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))

class SendText2(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    html = request.POST['html']
    rawText = request.POST['text']
    tipo_analisis = request.POST['tipo_analisis']
    data = {
      'html': html.encode('utf8'),
      'tipo_analisis': self.postAnalisis(rawText, html, tipo_analisis),
    }
    return Response(data, status.HTTP_201_CREATED)

  def postAnalisis(self, rawtext, html, tipo_analisis):
    url = 'http://redilegra.com/'+tipo_analisis
    payload = {'texto': rawtext, 'html': html}
    res = requests.post(url, data=payload)
    return json.loads(res.text.encode('utf8'))


class Proposito(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    html = request.POST['html']
    text = request.POST['text']
    macromovida = request.POST['macromovida']
    data = {'proposito': self.postAnalisis(text, html, "proposito", macromovida)}
    return Response(data, status.HTTP_201_CREATED)

  def postAnalisis(self, rawtext, html, endpoint, macromovida):
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
