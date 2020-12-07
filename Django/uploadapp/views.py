from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from wsgiref.util import FileWrapper
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from .extract import unzip, redPlag
from .models import File
# from .extract import unzip
# Create your views here.

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self,request,*args,**kwargs):
        file_serializer = FileSerializer(data=request.data)
        # print(file_serializer)

        if(file_serializer.is_valid()):
            file_serializer.save()  
            unzip(request.FILES['file'].name)
            redPlag("unzipped")
            return Response(file_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args,**kwargs):
        print(kwargs['file_name'])
        file_name=kwargs['file_name']
        # file=File.objects.get(name=kwargs['file_name'])
        path="part1/testing.png"
        print("path is ",path)
        response = HttpResponse(open(path,'rb').read(),content_type="application/force-download")
        response['Content-Disposition'] = 'attachment; filename=redplag.png'
        return response






