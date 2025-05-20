import boto3
from uuid import uuid4
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, REGION_NAME

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


def upload_image_to_s3(file):
    filename = f"posts/{uuid4().hex}_{file.filename}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
    url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
    return url


def delete_s3_file(file_url):
    file_key = file_url.split(f"{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/")[-1]

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
    except Exception:
        pass
