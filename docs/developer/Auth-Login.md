# 🚪 Authentication and Login

The application uses authentication with **JWT (JSON Web Tokens)** to secure endpoints. Each request to a protected resource must include a JWT token, signed by the backend's private key, which contains the user's role. This ensures that only tokens issued by the backend can access protected resources.

## 👱✔️ Development Authentication Guide

### 🖥 Using Backend Swagger Docs

To authenticate via Swagger docs, located at `http://localhost:8000/docs`, follow these steps:

1. **Create a user**:
   Use the user creation endpoint to create a user. This endpoint should remain unprotected during development.

2. **Login to get JWT Token**:
   Go to the login endpoint and enter the created user's credentials (only username and password are required). After submitting, you will receive a JWT token.

3. **Authorize Swagger requests**:
   Click the `Authorize` button in the top-right corner of Swagger UI, and paste the JWT token into the authorization dialog. You are now authenticated in the Swagger docs as the logged-in user.

### 📺 Frontend Authentication

For frontend authentication, you can:

- **Register and log in** through the UI:
  Users can register and log in via the frontend interface.

- **Login via Swagger docs**:
  Alternatively, you can use the steps above to log in via Swagger, and the resulting JWT token can be used for frontend requests.

## 🔒 Internal Behaviour

### 🖥 Backend JWT Handling

Protected backend endpoints use the following structure for authentication:

```python
token: Annotated[TokenData, Depends(JWTBearer())]
```

This parameter relies on the `JWTBearer` class to handle authentication. The `JWTBearer` class:

- **Validates the JWT**: Ensures the token is signed by the backend and has not expired.
- **Supports Authorization Header and Cookies**: The JWT token can be passed either via the Authorization header or stored in cookies.

### 🌐 Frontend JWT Handling

Login can be done in two ways:

- **Introducing an existing user and password**
- **Auto login made if there's a JWT Token stored in localStorage**

Upon successful login, the JWT token provided by backend response is:

- **Stored in an HTTP-only cookie**: This cookie is automatically sent with each outgoing request to secure backend endpoints.
- **Stored in localStorage**: The token is also stored in the browser's localStorage to enable features such as auto-login after page reloads.

The HTTP-only cookie enhances security by preventing JavaScript access to the JWT token, mitigating the risk of XSS (Cross-Site Scripting) attacks.

### 🧪 Testing handling

Now that we know certain backend endpoints are protected we have to adapt our tests. For authenticating during tests we need to add the following header:

```python

headers = "authorization": f"Bearer {jwt}", # -> INCLUDE JWT Token here

def get_user(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/users/{name}", headers=headers)
```
