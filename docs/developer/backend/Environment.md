# ❗ Environment

In this document we will cover:

- How to use environment variables
- Environment variables usage
- Development environment variables

## 🖐️ How to use environments

The file should contain key-value pairs, with each pair on a separate line and the key and value separated by an equals sign (`=`). For example:

```console
KEY1=value1
```

### For App local development

Backend app will look for `.env` file under `Backend/` folder

- Copy `docker/env/dev.env` to `Backend/` and rename it to `.env`

_Note that file has to be named `.env` not `dev.env` or similars, having a different name will not make its variables part of the environment variables_ recognized by the backend.

### For Docker

Backend app will look for `[dev|prod].env` file under `Backend/docker/env` folder

- `dev.env` for development
- `prod.env` for production

## 📄 Environments variables

In this section we will explain the meaning and the usage of the environment variables. Some of them are only necessary for one [architecture](../Architecture.md), this means you can not declared them at all at the `.env` file.

### ➡️ Commons

- **MONGO_URI**: the database connection URI such as `mongodb://root:root@mongodb:27017/`, this will connect backend into the selected database for storing all persistent data.
- **SECRET_KEY_SIGN**: 32 byte key(16 characters) for signing JWT Tokens that will authenticate the user. You can use `f24e2f3ac557d487b6d879fb2d86f2b2` as an example. This key will make sure the JWT Tokens are provided by our backend and not someone else's. For generating a new secret use `openssl rand -hex 16`.
- **ENV_VALUE**: determines the current environment of the app, it can be:
  - `PROD`: production environment.
  - `DEV`: development environment. Enables hot reload.
- **ARCH**: the song architecture selected, it can be one of the following [architectures](../Architecture.md):
  - `BLOB(Recommended for production and development)`: song architecture that stores songs in database and streams them using an endpoint.
  - `SERVERLESS`: (deprecated) song architecture using AWS Serverless Function with streaming.

### ➡️ Streaming using AWS Serverless Functions (`SERVERLESS`)(deprecated)

- **SERVERLESS_FUNCTION_URL**: the url of the AWS serverless function (Lambda) that manages songs and comunicates with cloud storage.

```
ARCH=SERVERLESS
```

## ⚒️ DEVELOPMENT ENVIRONMENT

The following file can be used out of the box for development purpouse. It contains the following characteristics:

- **Local MongoDB database**. Use local MongoDB database, you can deploy one using our Docker stack as described [here](Docker.md).
- **Ready to use secret key**
- **BLOB architecture selected**. This will only make necessary a MongoDB database because no cloud services are used in this architecture.
- **DEV** mode. It will enable hot reload for FastAPI.

[Development environment file](https://github.com/AntonioMrtz/SpotifyElectron/blob/master/Backend/docker/env/dev.env)

## ✅ PRODUCTION ENVIRONMENT

The following file can be used out of the box for development purpouse. It contains the following characteristics:

- **Remote MongoDB database**. Use a remote MongoDB production ready database. Replace both `root` in `mongodb://root:root@mongodb:27017/` with MongoDB instance user and password respectively.
- **Ready to use secret key**. Generate it using `openssl rand -hex 16`.
- **BLOB architecture selected**. Use streaming architecture using BLOB files.
- **PROD** mode. It will disable hot reload for FastAPI.

Production introduces two new environment values for configuring MongoDB database:

- **MONGO_INITDB_ROOT_USERNAME**: MongoDB user, must match the one provided in MONGO_URI
- **MONGO_INITDB_ROOT_PASSWORD**: MongoDB password, must match the one provided in MONGO_URI

If I have an user `user` with password `password` I have to set the following environments:

```
MONGO_INITDB_ROOT_USERNAME=user
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_URI=mongodb://user:password@mongodb:27017/
```

[Development environment file](https://github.com/AntonioMrtz/SpotifyElectron/blob/master/Backend/docker/env/prod.env)
