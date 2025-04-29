import requests
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

# Fill thông tin Bucket
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_BUCKET_NAME = 'hopehub-storage'

r2_client = boto3.client('s3',
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY
)

R2_PUBLIC_BASE = "https://hopehub-storage.c9ac3686ee9b83a90c8f01bd6cd077fa.r2.cloudflarestorage.com/MEDIA"

# Mapping nguồn tương ứng file trên R2
SOURCE_TO_FILE = {
    "xvideos": "Xvideos/xvideos_media.json",
    "redgifs": "Redgifs/redgifs_media.json",
    "pornhub": "Pornhub/pornhub_media.json",
}

def fetch_media_from_r2(source):
    try:
        res = r2_client.get_object(Bucket=R2_BUCKET_NAME, Key="BIN/bins_real_full.json")
        data = res['Body'].read().decode('utf-8')
        return json.loads(data)
    except Exception as e:
        print(f"[Error] Fetch R2 {source}: {e}")
        return None
