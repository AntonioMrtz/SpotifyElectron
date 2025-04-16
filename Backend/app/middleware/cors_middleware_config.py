"""CORS Middleware configurations"""

allowed_origins = [
    "http://localhost/",
    "http://localhost:1212",
    "https://localhost:1212/",
    "https://localhost",
    "https://localhost:1212",
    "https://localhost:1212/",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000",
]

allow_credentials = True
allowed_methods = ["POST", "GET", "PUT", "DELETE", "PATCH"]
max_age = 3600
allowed_headers = ["*"]
