# Environment

In this document we will cover:

- How to use environment variables
- Environment variables usage
- Development environment variables

## 🖐️ How to use environments

To use environments in the app, you will need to place a file named `.env` under the `Backend` folder. The file should contain key-value pairs, with each pair on a separate line and the key and value separated by an equals sign (`=`). For example:

```console
KEY1=value1
```

_Note that file has to be named `.env` not `.env.local` or similars, having a different name will not make its variables part of the environment variables_ recognized by the backend.

## 📄 Environments variables

In this section we will explain the meaning and the usage of the environment variables. Some of them are only necessary for one [architecture](../Architecture.md), this means you can not declared them at all at the `.env` file.

### ➡️ Commons

- **SECRET_KEY_SIGN**: 32 byte key(16 characters) for signing JWT Tokens that will authenticate the user. You can use `f24e2f3ac557d487b6d879fb2d86f2b2` as an example. This key will make sure the JWT Tokens are provided by our backend and not someone else's. For generating a new secret use `openssl rand -hex 16`.
- **ENV_VALUE**: determines the current environment of the app, it can be:
  - `PROD`: production environment.
  - `DEV`: development environment. Enables hot reload.
- **ARCH**: the song architecture selected, it can be one of the following [architectures](../Architecture.md):
  - `BLOB(Recommended for production and development)`: song architecture that stores songs in database and streams them using an endpoint.
  - `SERVERLESS`: (deprecated) song architecture using AWS Serverless Function with streaming.

### ➡️ No streaming with songs stored in database (`BLOB`)

- **MONGO_URI**: the database connection URI such as `mongodb://root:root@localhost:27017/`, this will connect backend into the selected database for storing all persistent including the song files.

```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
ENV_VALUE=DEV
ARCH=BLOB
```

### ➡️ Streaming using AWS Serverless Functions (`SERVERLESS`)(deprecated)

- **SERVERLESS_FUNCTION_URL**: the url of the AWS serverless function (Lambda) that manages songs and comunicates with cloud storage.
- **MONGO_URI**: the database connection URI such as `mongodb://root:root@localhost:27017/`, this will connect backend into the selected database for storing all persistent data but not including song files.

```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
SERVERLESS_FUNCTION_URL=https://lambda-url.us-east-1.on.aws/path/
ENV_VALUE=DEV
ARCH=SERVERLESS
```

## ⚒️ DEVELOPMENT ENVIRONMENT

The following file can be used out of the box for development purpouse. It contains the following characteristics:

- **Local MongoDB database**. Use local MongoDB database, you can deploy one using our Docker stack as described [here](Docker.md).
- **Ready to use secret key**
- **BLOB architecture selected**. This will only make necessary a MongoDB database because no cloud services are used in this architecture.
- **DEV** mode. It will enable hot reload for FastAPI.

```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
ENV_VALUE=DEV
ARCH=BLOB
```

## ✅ PRODUCTION ENVIRONMENT

The following file can be used out of the box for development purpouse. It contains the following characteristics:

- **Remote MongoDB database**. Use a remote MongoDB production ready database.
- **Ready to use secret key**. Generate it using `openssl rand -hex 16`.
- **BLOB architecture selected**. Use streaming architecture using BLOB files.
- **PROD** mode. It will disable hot reload for FastAPI.

```
MONGO_URI=mongodb://root:root@remote:27017/
SECRET_KEY_SIGN=generated-key
ENV_VALUE=PROD
ARCH=BLOB
```

## 🪨 ALL ROUND ENVIRONMENT

You can also use the following `.env` file for changing between architectures as it contains all the variables needed. Just be sure to fill the the needed environments for the architecture seleted.

```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
SERVERLESS_FUNCTION_URL=https://lambda-url.us-east-1.on.aws/path/
ENV_VALUE=DEV
ARCH=BLOB
```
