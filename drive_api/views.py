from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drive_api.serializers import FileSerializer
from drive_api.utils import upload_to_google_drive


@swagger_auto_schema(method='post', request_body=FileSerializer)
@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        data = request.data
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            file_name = data.get('name')
            file_data = data.get('data')
            upload_to_google_drive(name=file_name, data=file_data)
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
