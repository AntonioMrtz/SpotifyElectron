# Set up and run BACKEND

In this section we will cover:

- How to set up the proyect
- Run the proyect and debug
- Deploy docker containers for development and production

## 🛠 Set up the proyect

### 1. Enter backend directory

```
cd Backend
```

### 2. Rename `.env.local` to `.env` for development or create an enviroment file in root path

* More on enviroments [here](Enviroment.md).
* A development-ready `.env` file is also provided in the document.

The enviroment variables are the following:

```
* MONGO_URI= uri for connecting into a MongoDB database ( mongodb://root:root@localhost:27017/ )
* SECRET_KEY_SIGN= 32 byte key for signing tokens in backend
* SERVERLESS_FUNCTION_URL= URL of Serverless/Lambda API for accesing AWS services and managing song ( only needed in STREAMING_SERVERLESS_FUNCTION architecture )
* ARCH= song architecture ( STREAMING_SERVERLESS_FUNCTION | BLOB )
* ENV_VALUE= prod or development ( PROD | DEV )

```

### 3. Install the virtual enviroment and dependencies

🪟 **Windows**
```
python -m venv venv;
venv/Scripts/activate;
pip install -r requirements.txt;
pip install -r requirements-dev.txt;
pip install -r requirements-test.txt;

```

🐧 **Linux**
```
python3.11 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
pip install -r requirements-dev.txt &&
pip install -r requirements-test.txt
```
There's included a script `install-all-requirements.sh` that install all dependencies from a given directory in an already create virtual enviroment (Folder has to be named `venv`). Works both for Windows and Linux.


### 4. Run the app in hot reload debug mode, launch the provided vscode script [**DEBUG Backend app**] or run:

```
python -m app
```

### 5. The app will be deploy at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**. API docs will be placed at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## 🐳 Docker deployment

In this section we will cover how to use Docker for local development or for production deployment. All the necessary tools for development such as a mongoDB database is provided with the dev enviroment script described below. For more info check the [extended docker documentation](Docker.md).

1. Go to docker folder

```
cd docker/
```

### Development Enviroment

For development it is recommended to deploy the dev enviroment containers that provide:

- Local MongoDB Database
- Mongo Express administration dashboard
  - Connect [http://localhost:8081/](http://localhost:8081/)
  - Use user : admin and password : pass
- Backend Server ( stop this container if backend server is running locally already )

Run this command to build and up the development containers

```
./build_and_up_dev.sh
```

### Production Enviroment

In production it is recommended to connect to a remote database, the prod enviroment provide:

- Backend Server

```
./build_and_up_prod.sh
```
