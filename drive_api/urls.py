from django.urls import path

from drive_api.apps import DriveApiConfig
from drive_api.views import upload_file

app_name = DriveApiConfig.name

urlpatterns = [
    path('drive_api/upload/', upload_file, name='upload_file')
]