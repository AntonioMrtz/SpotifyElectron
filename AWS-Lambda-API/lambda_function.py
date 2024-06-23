"""
Lambda function for handling Song Cloud resources
"""

import base64
import json
import os

import boto3

from constants import (
    BUCKET_BASE_PATH,
    BUCKET_NAME_ENV_PATH,
    CLOUDFRONT,
    CLOUDFRONT_DISTRIBUTION,
    CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME,
    DISTRIBUTION_ID_ENV_PATH,
    S3,
)

s3 = boto3.resource(S3)
s3_client = boto3.client(S3)
song_bucket = s3.Bucket(os.getenv(BUCKET_NAME_ENV_PATH))
distribution_id = os.getenv(DISTRIBUTION_ID_ENV_PATH)
cloudfront_client = boto3.client(CLOUDFRONT)

cloudfront_domain_name = cloudfront_client.get_distribution(Id=distribution_id)[
    CLOUDFRONT_DISTRIBUTION
][CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME]


def get_cloudfront_url(resource_path: str) -> str:
    """Get cloudfront URL for a given resource

    Args:
        resource_path (str): the resource

    Returns:
        str: the cloudfront streaming URL associated with the given resource
    """
    cloudfront_url = (
        f"https://{cloudfront_domain_name}/{BUCKET_BASE_PATH}{resource_path}.mp3"
    )
    return cloudfront_url


def get_http_method_from_event(event) -> str:
    """Get HTTP method ( GET, POST...) from incoming event.

    Args:
        event : incoming event

    Returns:
        str: incoming HTTP method
    """
    try:
        http_method = event["requestContext"]["http"]["method"]
    except Exception:
        http_method = event["httpMethod"]

    return http_method


def lambda_handler(event, context) -> dict:
    """Handles the incoming requests

    Args:
        event (_type_): info about the incoming request
        context (_type_):

    Returns:
        dict: the response data
    """
    try:
        http_method = get_http_method_from_event(event)
        song_name = event["queryStringParameters"]["nombre"]

        if http_method == "GET":
            return {
                "statusCode": 200,
                "body": json.dumps({"url": str(get_cloudfront_url(song_name))}),
            }

        elif http_method == "DELETE":
            s3_client.delete_object(
                Bucket=song_bucket.name, Key=f"{BUCKET_BASE_PATH}{song_name}.mp3"
            )
            return {
                "statusCode": 202,
                "body": json.dumps({"details": "Song deleted successfully"}),
            }

        elif http_method == "POST":
            song_key = f"{BUCKET_BASE_PATH}{song_name}.mp3"
            body_str = event["body"]
            body_dict = json.loads(body_str)
            song_data = body_dict.get("file")
            encoded_data = song_data.split("'")[1]

            decoded_bytes = base64.b64decode(encoded_data)

            s3_client.put_object(
                Body=decoded_bytes, Bucket=song_bucket.name, Key=song_key
            )
            return {
                "statusCode": 201,
                "body": json.dumps({"details": "Song upload successfully"}),
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
