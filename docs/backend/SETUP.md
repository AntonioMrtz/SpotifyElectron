# Set up and run BACKEND

In this section we will cover:

- How to set up the proyect
- Deploy docker containers for development and production

## 🛠 Set up the proyect

### 1. Enter backend directory

```console
cd Backend/
```

### 2. Launch Backend dependencies using Docker

This will launch all required dependencies such as MongoDB database for local development

```console
cd Backend/docker/;
./build_and_up_dev_backend.sh;
```

* More on Docker in [Docker docs](Docker.md).


### 3. Get or create `.env` file under `Backend/

Development ready enviroment is provided at `Backend/docker/`. Copy and rename it to `.env` using the following command:

```console
cd Backend/docker/;
cp env/dev.env ../.env;
```

* Check upstream [development environment file](https://github.com/AntonioMrtz/SpotifyElectron/blob/master/Backend/docker/env/dev.env)

* More on environments in [environment docs](Environment.md).


### 4. Install the virtual environment and dependencies

🪟 **Windows**
```console
cd Backend/;
python -m venv venv;
venv/Scripts/activate;
pip install -r requirements.txt;
pip install -r requirements-dev.txt;
pip install -r requirements-test.txt;

```

🐧 **Linux**
```console
cd Backend/ &&
python3.11 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
pip install -r requirements-dev.txt &&
pip install -r requirements-test.txt
```
There's included a script `install-all-requirements.sh` that install all dependencies from a given directory in an already create virtual environment (Folder has to be named `venv`). Works both for Windows and Linux.


### 5. Run the app:

* App will be launched at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Swagger docs will be launched at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


#### Standar with hot reload
This will automatically reload the app if changes are made.

```console
python -m app
```

#### Debug

Launch the app in **debug mode** using `DEBUG Backend app` at VSCODE debug section. Breakpoints selected in code will be triggered.
