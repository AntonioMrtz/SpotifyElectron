# Set up and run BACKEND

In this section we will cover:

* How to set up the proyect
* Run the proyect and debug
* Deploy docker containers for development and production
* Run tests
* Access documentation

## 🛠 Set up the proyect

### 1. Enter backend directory

```
cd Backend
```

### 2. Rename `.env.local` to `.env` for development or create the enviroment file in root path with the following data. More on enviroments [here](Enviroment.md). A development-ready `.env` file is also provided in the document.


### 3. Install the virtual enviroment and dependencies

```
python -m venv venv;
venv/Scripts/activate;
pip install -r requirements.txt;
pip install -r requirements-dev.txt;
pip install -r requirements-test.txt;

```
### 4. Run the app in hot reload debug mode, launcht the provided vscode script or run:

```
python -m app
```

### 5. The app will be deploy at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**. API docs will be at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**


## 🐳 Docker deployment

In this section we will cover how to use Docker for local development or for production deployment. All the necessary tools for development such as a mongoDB database is provided with the dev enviroment script described below. For more info check the [extended docker documentation](Docker.md).

1. Go to docker folder
```
cd docker/
```

### Development Enviroment (RECOMMENDED for DEVELOPMENT)

For development it is recommended to deploy the dev enviroment containers that provide:

* Local MongoDB Database
* Mongo Express administration dashboard
  * Connect [http://localhost:8081/](http://localhost:8081/)
  * Use user : admin and password : pass
* Backend Server ( stop this container if backend server is running locally already )

Run this command to build and up the development containers
```
./build_and_up_dev.sh
```

### Production Enviroment

In production it is recommended to connect to a remote database, the prod enviroment provide:

* Backend Server
```
./build_and_up_prod.sh
```

## 📓 Access API Swagger documentation

* Swagger: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**


## ⚓ Pre-commit

Pre-commit is used for ensuring code quality before it gets commited. When you install pre-commit hooks a check will be triggered before commiting ensuring the rules specified in `.pre-commit-config.yaml`, if the check fails the commit wont be submitted. By default pre-commit will check the linting and formatting of the code that its going to be commited.

#### 1. Install pre-commits hooks

```
pre-commit install
```

#### 2. Force pre-commit run on all files


```
pre-commit run --all-files
```


## 🎨 Run style and linting on code

### 1. Run style rules and sort imports
```
python -m ruff format
```

### 2. Run linting

```
python -m ruff check --fix
```


## ✏ Install the recommended extensions for VSCODE

1. Go to extensions
2. Select filter extensions
3. Recommended
4. Workspace recommended
5. Install workspace recommended
