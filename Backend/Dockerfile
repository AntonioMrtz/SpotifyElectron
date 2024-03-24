
FROM python:3.11-slim

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

WORKDIR /code/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


#docker build -t spotify_electron_backend_image .
#docker run -d --name spotify_electron_backend -e MONGO_URI=mongo-uri SECRET_KEY_SIGN=secret-key-sign LAMBDA_URL=lambda-url ARCH=STREAMING_LAMBDA ENV_VALUE=PROD -p 8000:8000 spotify_electron_backend_image
