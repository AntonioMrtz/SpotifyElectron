
FROM python:3-slim-buster

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /code/app

WORKDIR /code/
CMD ["python", "-m", "app"]

#docker build -t spotify_electron_backend_image .
#docker run -d --name spotify_electron_backend -e MONGO_URI=mongo-uri SECRET_KEY_SIGN=secret-key DISTRIBUTION_ID=cloudfront-distribution-id -p ARCH=STREAMING_SDK ENV_VALUE=PROD 8000:8000 spotify_electron_backend_image
