# 1. Setup and run BACKEND

In this section we will cover:

* How to setup the proyect
* Run the proyect and debug
* Run tests
* Access documentation
* Containerize

## 🛠 Setup the proyect

1. Enter backend directory 

```
cd Backend API;
```

2. Create the enviroment file in root path with the following data. **Check .env.example file to see format**

```
* MONGO_URI= uri for connecting into a MongoDB database
* SECRET_KEY_SIGN= 32 byte key for signing tokens in backend
* LAMBDA_URL= URL of Lambda API for accesing AWS services and managing song

```

3. Install the virtual enviroment and dependencies 

```
python -m venv venv;
venv/Scripts/activate
pip install -r requirements.txt;
pip install -r requirements_dev.txt;
pip install -r requirements_test.txt;
```
4. Run the app in hot reload debug mode 

```
cd src/;
python3 -m uvicorn main:app --reload;
```

5. The app will be deploy at **http://127.0.0.1:8000/**

## 📓 Access documentation and swagger interface

* Swagger: **http://127.0.0.1:8000/docs**
* Auto-generated documentation: **Backend API/api-docs-spotify-electron.html**

## ✔️ Run tests

1. Go to src folder
```
cd src/;
```
2. Run tests
```
python -m pytest . // Normal test run

or

python -m pytest --cov=. --cov-report=html // Test run and generate coverage in folder src/htmlcov/index

```

## ✏ Install the recommended extensions for VSCODE 

1. Go to extensions
2. Select filter extensions
3. Recommended
4. Workspace recommended
5. Install workspace recommended

## 🐳 Containerize the app

### Dev Enviroment

1. Go to docker folder
```
cd docker/
```

2. Run docker compose with the script build_and_up
```
docker build -t spotify_electron_backend_image .
```


### Production Enviroment

1. Build the image
```
docker build -t spotify_electron_backend_image .
```

2. Run the container with the enviroment variables
```
docker run -d --name spotify_electron_backend -e MONGO_URI=mongo-uri SECRET_KEY_SIGN=secret-key-sign LAMBDA_URL=lambda-url -p 8000:8000 spotify_electron_backend_image

```
