# ⚙️ Set up and run BACKEND

In this section we will cover how to set up the backend of the application.

## 🛠 Set up the proyect

### 1. Enter backend directory

```console
cd Backend/
```

### 2. Launch Backend dependencies using Docker

This will launch all required dependencies such as MongoDB database for local backend development.

```console
cd Backend/docker/;
./build_and_up_dev_backend.sh;
```

* Learn more about other Docker configurations for the application in [Docker docs](Docker.md).


### 3. Get or create `.env` file under `Backend/

A development ready environment files is provided at `Backend/docker/`. The environment files has to be placed under `Backend/` folder and should be named `.env`. It can be done using the following command:

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
pip install -r requirements-dev.txt

```

🐧 **Linux**
```console
cd Backend/ &&
python3.12 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
pip install -r requirements-dev.txt
```


### 5. Run the app:

* App will be launched at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Swagger docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


#### Standar with hot reload
This will automatically reload the app if changes are made.

```console
python -m app
```

#### Debug

Launch the app in **debug mode** using `DEBUG Backend app` at VSCODE debug section. Breakpoints selected in code will be triggered.
