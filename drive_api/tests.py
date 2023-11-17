from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from config import settings
from drive_api.models import File
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class UploadFileIntegrationTest(TestCase):
    """
    Integration tests for the file upload functionality.
    This class contains tests for uploading files, validating responses,
    listing files from Google Drive, and deleting uploaded files.
    """

    def test_upload_file_integration(self):
        """
        Test the flow of uploading a file, listing it, and then deleting it.
        This method ensures that the file upload view works correctly,
        the uploaded file is listed on Google Drive, and it can be deleted.
        """
        file_data = {'name': 'Test name', 'data': 'Test data'}

        response_post = self.client.post(reverse('drive_api:upload_file'), data=file_data, format='json')
        self.assertEquals(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response_post.json()['message'], 'File uploaded successfully')
        self.assertTrue(File.objects.filter(name=file_data['name']).exists())

        drive_service = self.get_drive_service()
        file_list = self.list_files(drive_service)
        self.assertIn(file_data['name'], file_list)

        self.delete_file(drive_service, file_data['name'])

        file_list_after_deletion = self.list_files(drive_service)
        self.assertNotIn(file_data['name'], file_list_after_deletion)

    def test_upload_file_invalid_data(self):
        """
        Test the handling of invalid data when uploading a file.
        This method checks both 'name' and 'data' have been provided.
        """
        file_data_no_name = {'data': 'Test data'}
        response_post = self.client.post(reverse('drive_api:upload_file'), data=file_data_no_name, format='json')
        self.assertEquals(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response_post.json()['name'], ['This field is required.'])

        file_data_no_data = {'name': 'Test name'}
        response_post = self.client.post(reverse('drive_api:upload_file'), data=file_data_no_data, format='json')
        self.assertEquals(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response_post.json()['data'], ['This field is required.'])

    @staticmethod
    def get_drive_service():
        """
        Get an instance of the Google Drive API service.
        This method creates and returns an instance of the Google Drive API service
        using the credentials provided in the settings.
        """
        credentials = Credentials.from_authorized_user_info(
            {'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'scopes': [settings.SCOPES],
             'refresh_token': settings.REFRESH_TOKEN, 'token_uri': settings.TOKEN_URI})
        return build('drive', 'v3', credentials=credentials)

    @staticmethod
    def list_files(drive_service):
        """
        List files from Google Drive.
        This method uses the provided Google Drive API service to list all files
        and returns a list of their names.
        """
        files = drive_service.files().list().execute()
        return [file['name'] for file in files.get('files', [])]

    @staticmethod
    def delete_file(drive_service, file_name):
        """
        Delete a file from Google Drive.
        This method takes the name of a file, searches for it on Google Drive,
        and deletes it using the provided Google Drive API service.
        """
        files = drive_service.files().list(q=f"name='{file_name}'").execute()
        file_id = files.get('files', [])[0]['id']
        drive_service.files().delete(fileId=file_id).execute()
