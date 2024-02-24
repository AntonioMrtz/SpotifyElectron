#
FROM python:3-slim-buster

#
WORKDIR /app

#
COPY ./requirements.txt /app/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#
COPY ./src /app/src

#
WORKDIR /app/src

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#docker build -t spotify_electron_backend_image .
#docker run -d --name spotify_electron_backend -e MONGO_URI=mongo-uri SECRET_KEY_SIGN=secret-key-sign LAMBDA_URL=lambda-url -p 8000:8000 spotify_electron_backend_image
