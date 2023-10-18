import json
import boto3
import os
import io
import base64

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
song_bucket = s3.Bucket('canciones-spotify-electron')
bucket_base_path = "canciones/"
distribution_id = os.getenv("DISTRIBUTION_ID")

def get_cloudfront_url(resource_path:str):

    cloudfront_client = boto3.client('cloudfront')
    response = cloudfront_client.get_distribution(Id=distribution_id)
    domain_name = response['Distribution']['DomainName']

    # Construct the CloudFront URL
    cloudfront_url = f"https://{domain_name}/{bucket_base_path}{resource_path}.mp3"

    return cloudfront_url


def lambda_handler(event, context):

    try:

        request_data = event["requestContext"]["http"]

        path = request_data["path"]
        method = request_data["method"]

        if(method=='GET'):
            song_name = path.split("/")[-1]
            return get_cloudfront_url(song_name)

        elif(method=='DELETE'):
            song_name = path.split("/")[-1]
            s3_client.delete_object(Bucket=song_bucket.name, Key=f"{bucket_base_path}{song_name}.mp3")
            return {
                "statusCode": 202,
                "body": json.dumps({"details": "Canción borrada correctamente"})
            }

        elif(method=='POST'):

            input_params = event["queryStringParameters"]

            song_key = f"{bucket_base_path}{input_params['nombre']}.mp3"

            body_str = event["body"]
            body_dict = json.loads(body_str)
            song_data = body_dict.get("file")
            song_data = song_data.encode()

            byte_stream = io.BytesIO(song_data)

            read_song_data = byte_stream.read()

            s3_client.put_object(Body=read_song_data, Bucket=song_bucket.name, Key=song_key)

            return {
                "statusCode": 201,
                "body": json.dumps({"details": "Canción creada correctamente"})
            }

        return path

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



