import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

CREDENTIALS_FILE = 'credentials.json'  # File credentials Google
FOLDER_ID = '1qYDmgDAv56HmRevKei1d8SexTmNujxYp'  # ID thư mục Drive đã chia sẻ

def upload_file_to_drive(local_file_path, file_name=None, mimetype='application/octet-stream'):
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name or os.path.basename(local_file_path),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(local_file_path, mimetype=mimetype)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    service.permissions().create(
        fileId=file['id'],
        body={'role': 'reader', 'type': 'anyone'}
    ).execute()

    file_id = file.get('id')
    return f"https://drive.google.com/uc?id={file_id}"