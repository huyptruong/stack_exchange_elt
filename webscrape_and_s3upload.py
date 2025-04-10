import boto3
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os
from io import BytesIO
from datetime import datetime, timezone

# Load the .env.local file for AWS credentials
load_dotenv(dotenv_path=".env.local")

# Initialize AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Function to upload data to S3
def upload_data_to_s3(data, bucket, object_name):
    """
    Uploads data (binary) to an S3 bucket.

    :param data: The data to upload (binary format)
    :param bucket: S3 bucket to upload to
    :param object_name: The S3 object name (filename)
    :return: True if data was uploaded, else False
    """
    try:
        s3.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=data
        )
        print(f"Data uploaded to '{bucket}/{object_name}' successfully.")
        return True
    except NoCredentialsError:
        print("Credentials not available.")
        return False

# Function to fetch answers for a specific question
def fetch_answers(question_id):
    # Base URL for answers
    answers_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"

    # Set up parameters for the answers request
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "gardening.stackexchange.com",
        "filter": "withbody"  # Include the answer body
    }

    try:
        # Get answers for the question
        response = requests.get(answers_url, params=params)
        response.raise_for_status()

        # Parse the JSON response for answers
        answers_data = response.json().get("items", [])

        answers_list = []

        if answers_data:
            for answer in answers_data:
                answer_body_html = answer["body"]
                answer_score = answer["score"]

                # Convert HTML body to plain text
                answer_text = BeautifulSoup(answer_body_html, "html.parser").get_text()

                answers_list.append({
                    "score": answer_score,
                    "answer": answer_text
                })

        return answers_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching answers for question {question_id}: {e}")
        return []

# Function to fetch recent questions and answers from Gardening Stack Exchange
def fetch_questions_and_answers(pagesize=5, tagged=None, page=1):
    # Base URL for questions
    questions_url = "https://api.stackexchange.com/2.3/questions"

    # Set up parameters for the question request
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "gardening.stackexchange.com",
        "pagesize": pagesize,
        "page": page,
        "filter": "withbody"  # Include the question body
    }

    # Add optional tagged filter
    if tagged:
        params["tagged"] = tagged

    try:
        # Get recent questions
        response = requests.get(questions_url, params=params)
        response.raise_for_status()

        # Parse the JSON response for questions
        questions_data = response.json().get("items", [])

        all_data = []

        # Process each question and fetch its answers
        for question in questions_data:
            question_id = question["question_id"]
            title = question["title"]
            body_html = question["body"]
            link = question["link"]
            tags = question["tags"]
            score = question["score"]

            # Convert HTML body to plain text
            body_text = BeautifulSoup(body_html, "html.parser").get_text()

            question_data = {
                "title": title,
                "link": link,
                "tags": tags,
                "score": score,
                "question": body_text
            }

            # Fetch answers for the current question
            answers_data = fetch_answers(question_id)
            question_data["answers"] = answers_data

            all_data.append(question_data)

        # Convert all data to a DataFrame
        df = pd.json_normalize(all_data)

        # Convert DataFrame to Parquet format
        buffer = BytesIO()
        df.to_parquet(buffer, engine='pyarrow', index=False)
        buffer.seek(0)

        # Upload the Parquet file to S3
        bucket_name = 'stackexchangegardening'
        timestamp   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        object_name = f"parquet_files_only/{timestamp}_page_{page}.parquet"

        upload_data_to_s3(buffer.getvalue(), bucket_name, object_name)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")

# Fetch questions and answers 
fetch_questions_and_answers(page=1)
#fetch_questions_and_answers(page=2)
#fetch_questions_and_answers(page=3)
