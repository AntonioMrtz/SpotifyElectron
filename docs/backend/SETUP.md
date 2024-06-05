# 1. Set up and run BACKEND

In this section we will cover:

* How to set up the proyect
* Run the proyect and debug
* Deploy docker containers for development and production
* Run tests
* Access documentation

## 🛠 Set up the proyect

1. Enter backend directory

```
cd Backend;
```

2. Use .env.local renaming it to .env for development or create the enviroment file in root path with the following data.

```
* MONGO_URI= uri for connecting into a MongoDB database ( mongodb://root:root@localhost:27017/ )
* SECRET_KEY_SIGN= 32 byte key for signing tokens in backend
* SERVERLESS_FUNCTION_URL= URL of Serverless/Lambda API for accesing AWS services and managing song ( only needed in STREAMING_SERVERLESS_FUNCTION architecture )
* ARCH= song architecture ( STREAMING_SERVERLESS_FUNCTION | BLOB )
* ENV_VALUE= prod or development ( PROD | DEV )

```

3. Install the virtual enviroment and dependencies

```
python -m venv venv;
venv/Scripts/activate;
pip install -r requirements.txt;
pip install -r requirements-dev.txt;
pip install -r requirements-test.txt;

```
4. Run the app in hot reload debug mode

```
python -m app;
```

5. The app will be deploy at **http://127.0.0.1:8000/**

6. You can also launch the app and tests with the VSCODE scripts included in the .vscode folder

## 🐳 Docker deployment

1. Go to docker folder
```
cd docker/
```

### Development Enviroment

For development it is recommended to deploy the dev enviroment containers that provide:
  * Local MongoDB Database
  * Mongo Express administration dashboard
      * Connect http://localhost:8081/
      * Use user : admin and password : pass
  * Backend Server ( stop this container if backend server is running locally already )

Run this command to build and up the development containers
```
./build_and_up_dev.sh
```

### Prod Enviroment

In production it is recommended to connect to a remote database, the prod enviroment provide:

  * Backend Server
```
./build_and_up_prod.sh
```

## 📓 Access documentation and swagger interface

* Swagger: **http://127.0.0.1:8000/docs**

## ✔️ Run tests

1. Run tests

Standar test run
```
python -m pytest tests/
```

Test run and generate code coverage in folder htmlcov/index.html
```
python -m pytest tests/ --cov=. --cov-report=html:tests/htmlcov

```
## ⚓ Pre-commit

### Set up

1. Install pre-commits hooks

```
pre-commit install
```
### Install

1. Force pre-commit run on all files


```
pre-commit run --all-files
```


## 🎨 Run style and linting on code

1. Run style rules and sort imports
```
python -m ruff format
```
2. Run linting

```
python -m ruff check --fix
```


## ✏ Install the recommended extensions for VSCODE

1. Go to extensions
2. Select filter extensions
3. Recommended
4. Workspace recommended
5. Install workspace recommended
