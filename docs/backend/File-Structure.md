# File Structure

In this document we will cover the file structure of the Backend for Spotify Electron.

## 🈴 App

- 📁 Common. Handles common logic for all app.
  - 📄 PropertiesManager: loads enviroment variables and its associated logic and stores global app states.
  - 📄 PropertiesMessageManager: loads and store common response messages.
- 📁 Database. Handles database connection.
- 📁 Exceptions. Custom base exceptions for our app.
- 📁 Logging. Configure and provide logging formatting and handling for all app modules.
- 📁 Middleware. Stores the middlewares used in the app and its logic.
- 📁 Patterns. Desing patterns schemas.
- 📁 Resources. Common configuration `.ini`.
- 📁 Spotify_electron: main folder for our bussiness logic.
  - 📁 Playlist. We will use playlist as an example but this apply to the whole domain model.
    - 📄 Controller. Router used by FastAPI, it handles the incoming HTTP Requests. Upon recieving HTTP Request it delegates into the service layer.
    -  Service. Handles the bussiness logic for our domain model. It communicates with the repository layer for dasta persistence.
    - 📄 Repository. Manages the persistence layer and communicates directly with the database.
    - 📄Schema. Stores the entity related model such as classes or exceptions.
    - 📁 Providers. Services responsible for loading or supplying services depending and database collections  multiple conditions.
    - 📁 Validations. Common validations for repository and service layer. This include among others checks for
    database responses.
  - 📁 Utils. Auxiliar functions for common operations such as date formatting, json validation...
- 📄`main`. Entrypoint of the app. Loads middlewares, routers and global configurations.

## 🐳 Docker

Docker folder contains configuration files and scripts for deploying app containers using Docker.
You can find more info [here](Docker.md).

## 🧪 Tests

Here we can find stuff related to testing our backend:

- 📁 `assets`. Folder that contains assets such as songs or files used in the tests.
- 📄 Test files. Test files are grouped by entities such as songs, database, playlist etc. Named with `test__testname` convention.
- 📁 `test_API`. Folder that stores shared logic between tests, such as HTTP requests.
- 📄 `conftest.py`. File that exposes fixtures to all test files.
- ⚙ `pytest.ini`. Config file for provided enviroment values on text execution.

## 🌳 Root Folder

In this folder we can find the Backend global configuration files. It includes:

- ⚙️ Ruff linter and formatter configuration file.
- ⚙️ Dependencies for base, dev and test mode. This follow the format `requirements-[type].txt`.
- 🏗️ Deploy configuration files such as Procfile and Dockerfile.
- ⚙️ Enviroment variables files. `.env.local` is used as an example, the app will only recognize `.env` files. More on [enviroments](Enviroment.md).

## ⚙️ .vscode

This folder is used to store the VSCODE related configurations. It contains:

- ⚙️ Recommended VSCODE extensions to use in the project
- ⚙️ Debug Scripts for launching the app and running the tests
- ⚙️ Settings for type checking python code and detecting tests files
