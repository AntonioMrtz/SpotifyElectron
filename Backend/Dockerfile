FROM python:3.12-slim AS builder

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN python -m pip wheel -r requirements.txt --no-cache-dir --no-deps --wheel-dir /wheels


FROM python:3.12-slim AS runner

WORKDIR /code
COPY --from=builder /wheels /wheels

RUN apt-get update && apt-get install -y curl && \
    python -m pip install --no-cache-dir /wheels/* && rm -r /wheels && \
    rm -rf /var/lib/apt/lists/*

COPY ./app /code/app

ENTRYPOINT [ "python", "-m", "app" ]
EXPOSE 8000

# For debugging purposes, you can uncomment this CMD
#CMD ["tail", "-f", "/dev/null"]

# Docker build command
# docker build -t spotify_electron_backend_image .
# Docker run command
# docker run -d --name spotify_electron_backend -e MONGO_URI=mongo-uri SECRET_KEY_SIGN=secret-key-sign SERVERLESS_FUNCTION_URL=serverless-function-url ARCH=BLOB ENV_VALUE=PROD -p 8000:8000 spotify_electron_backend_image
