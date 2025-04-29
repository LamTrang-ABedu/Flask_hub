import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load credentials
creds = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

# Khởi tạo Google Drive service
service = build('drive', 'v3', credentials=creds)

# ID của file bins_real_full.json trên Drive
BIN_FILE_ID = 'ID_FILE_CUA_BINS_REAL_FULL_JSON'

def fetch_bins_from_drive():
    try:
        request = service.files().get_media(fileId=BIN_FILE_ID)
        file_data = request.execute()
        bins = json.loads(file_data.decode('utf-8'))
        return bins
    except Exception as e:
        print(f"[Error] Fetch BINs from Drive: {e}")
        return []
