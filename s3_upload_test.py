import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

# Load the .env.local file
load_dotenv(dotenv_path=".env.local")

# Get the access key
access_key = os.getenv("ACCESS_KEY")

def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Uploads a file to an S3 bucket.

    :param file_name: Path to the file to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create the S3 client with explicit credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("AWS_REGION"))
        
    # Upload the file
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to '{bucket}/{object_name}' successfully.")
        return True
    except FileNotFoundError:
        print("The file was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False

# Replace with your file path, bucket name, and object name
file_name = 'requirements.txt'
bucket_name = 'stackexchangegardening'
object_name = 'uploaded-file.txt'  # Optionally specify an object name

# Upload the file
upload_file_to_s3(file_name, bucket_name, object_name)
