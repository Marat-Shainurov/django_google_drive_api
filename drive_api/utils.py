from io import BytesIO
from typing import Dict, Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from config import settings


def upload_to_google_drive(name: str, data: str) -> Dict[str, Any]:
    """
    Adds a new file to the Google Drive account.
    :param name: File name to upload
    :param data: File content to write
    """
    credentials = Credentials.from_authorized_user_info(
        {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'refresh_token': settings.REFRESH_TOKEN,
            'token_uri': settings.TOKEN_URI,
            'scopes': [settings.SCOPES]
        }
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.document'}
    media_body = MediaIoBaseUpload(BytesIO(data.encode('utf-8')), mimetype='text/plain')
    media = drive_service.files().create(body=file_metadata, media_body=media_body).execute()
    return media
