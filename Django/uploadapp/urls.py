from django.urls import path
from .views import FileUploadView

urlpatterns = [
    path('',FileUploadView.as_view(),name='post-fileuploadview'),
    path('<str:file_name>',FileUploadView.as_view(),name='get-fileuploadview'),
]