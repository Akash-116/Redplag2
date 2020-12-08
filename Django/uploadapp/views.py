from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from wsgiref.util import FileWrapper
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from .extract import unzip, redPlag, stubDownload
from .models import File
# Create your views here.

class FileUploadView(APIView):

    parser_classes = (MultiPartParser,)

    def post(self,request,*args,**kwargs):
        file_serializer = FileSerializer(data=request.data)
        # print(file_serializer)
        func_code = kwargs['func_code']
        print("FUNC_CODE is : ",  func_code)
        # stubpath = "stubcode/"

        if(func_code==5):

            if(file_serializer.is_valid()):
                file_serializer.save()  
                stubDownload(request.FILES['file'].name)
                # redPlag("unzipped","rpoutput", cplusplus, stub, "stubcode"  )
                return Response(file_serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        else:

            if(func_code == 0): 
                cplusplus=False
                stub=False
            elif(func_code == 1):
                cplusplus=True
                stub=False
            elif(func_code==2):
                cplusplus=False
                stub=True
            elif(func_code==3):
                cplusplus=True
                stub=True

            if(file_serializer.is_valid()):
                file_serializer.save()  
                unzip(request.FILES['file'].name)
                redPlag("unzipped","rpoutput", cplusplus, stub, "stubcode"  )
                return Response(file_serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args,**kwargs):
        file_name=kwargs['file_name']
        # print(file_name)
        # file=File.objects.get(name=kwargs['file_name'])
        path="rpoutput/testing."+file_name
        # print( "path is : ", path )
        response = HttpResponse(open(path,'rb').read(), content_type="application/force-download")
        response['Content-Disposition'] = 'attachment; filename=redplag.png'
        return response







