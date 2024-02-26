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
import pdb

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
        rawText = mammoth.extract_raw_text(docx_file).value
        html = mammoth.convert_to_html(docx_file).value
    if (file_extension == "txt"):
      txt_file = open('backendFondecyt/Docs/' + file_name, "r", encoding="utf-8")
      rawText = txt_file.read()
      html = ""
      for line in txt_file:
        stripped_line = line.rstrip()
        if (stripped_line.strip() != ""): 
          html += "<p>" + line + "</p>"
      txt_file.close()
    
    payload = {'texto': rawText, 'html': html}
    data = requests.post('http://redilegra.com/general', data=payload)
    data = json.loads(data.text.encode('utf8'))
    os.remove('backendFondecyt/Docs/' + file_name)
    return Response(data, status.HTTP_201_CREATED)
    

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
    
    payload = { 'html': html, 'texto': rawText }
    data = requests.post('http://redilegra.com/general', data=payload)
    data = json.loads(data.text.encode('utf8'))
    return Response(data, status.HTTP_201_CREATED)

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

class Conceptualizacion(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
      patron = request.POST['patron']
      anio = request.POST['anio']
      func = request.POST['funciones']
      data = self.PostConceptualizacion(patron, anio, func)
      return Response(data, status.HTTP_201_CREATED)

    def PostConceptualizacion(self, patron, anio, func):
      payload = {'patron': patron, 'anio': anio}
      if func == 'Indice':
        url = 'http://redilegra.com/indice'
      elif func == 'Extension':
        url = 'http://redilegra.com/extension'
      else:
        url = 'http://redilegra.com/indice' #Default a indice
      x = requests.post(url, data=payload)
      return json.loads(x.text.encode('utf8'))


class Ideacion(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    patron = request.POST['patron']
    anio = request.POST['anio']
    func = request.POST['funciones']
    data = self.PostIdeacion(patron, anio, func)
    return Response(data, status.HTTP_201_CREATED)

  def PostIdeacion(self, patron, anio, func):
    payload = {'patron': patron, 'anio': anio}
    if func == 'Títulos':
      url = 'http://redilegra.com/titulos'
    elif func == 'Palabras clave':
      url = 'http://redilegra.com/pclaves'
    elif func == 'Nubes conceptuales':
      url = 'http://redilegra.com/resumen'
    elif func == 'Hallazgos previos' or func == 'Espacios de contribución' or func == 'Relevancia investigaciones previas':
      payload['func'] = func
      url = 'http://redilegra.com/ideacion_func'


    else:
      url = 'http://redilegra.com/titulos'  # Default a indice
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))

class Transcripcion(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    patron = request.POST['patron']
    anio = request.POST['anio']
    mm = request.POST['macromove']
    func = request.POST['funciones']
    pasos = request.POST['pasos']
    data = self.PostTranscripcion(patron, anio, mm, func, pasos)
    return Response(data, status.HTTP_201_CREATED)

  def PostTranscripcion(self, patron, anio, mm, func, pasos):

    payload = {'patron': patron, 'anio': anio, 'macromove':mm, 'pasos':pasos}
    if func == 'Banco de frases':
      url = 'http://redilegra.com/flibro'
    elif func == 'Similitud de propósitos':
      url = 'http://redilegra.com/sem_similarity1'
    elif func == 'Patrones de propósitos':
      url = 'http://redilegra.com/pproposito'
      pass
    else:
      url = 'http://redilegra.com/indice'  # Default a indice
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))

class Reconceptualizacion(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, format=None):
    patron = request.POST['patron']
    func = request.POST['funciones']
    data = self.PostReconceptualizacion(patron, func)
    return Response(data, status.HTTP_201_CREATED)

  def PostReconceptualizacion(self, patron, func):
    payload = {'patron': patron}
    if func == 'Revisión de objetivo':
      url = 'http://redilegra.com/sem_similarity2'
    else:
      url = 'http://redilegra.com/indice'  # Default a indice
    x = requests.post(url, data=payload)
    return json.loads(x.text.encode('utf8'))