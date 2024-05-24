# Enviroment

In this document we will cover:

* How to use enviroment variables
* Enviroment variables usage
* Development enviroment variables

## How to use enviroments

To use environments in the app, you will need to place a file named `.env` under the `Backend` folder. The file should contain key-value pairs, with each pair on a separate line and the key and value separated by an equals sign (`=`). For example:

```
KEY1=value1
```

*Note that file has to be named `.env` not `.env.local` or similars, having a different name will not make its variables part of the enviroment variables* recognized by the backend.

## Enviroments variables

In this section we will explain the meaning and the usage of the enviroment variables. Some of them are only necessary for one [architecture](Architecture.md), this means you can not declared them at all at the `.env` file.

### Commons

 * **SECRET_KEY_SIGN**: 32 byte key for signing JWT Tokens that will authenticate the user. You can use `f24e2f3ac557d487b6d879fb2d86f2b2` as an example. This key will make sure the JWT Tokens are provided by our backend and not someone else's.
 * **ENV_VALUE**: determines the current enviroment of the app, it can be:
	* `PROD`: production enviroment.
	* `DEV`: development enviroment.
* **ARCH**: the song architecture selected, it can be one of the following [architectures](Architecture.md):
	* `STREAMING_LAMBDA`: song architecture using AWS Lambda with streaming.
	* `STREAMING_SDK`: song architecture using aws sdk with streaming.
	* `DB_BLOB`: song architecture with no streaming/cloud.

### Streaming using AWS Lambda (STREAMING_LAMBDA)

* **LAMBDA_URL**: the url of the AWS Lambda function that manages songs and comunicates with cloud storage.
* **MONGO_URI**: the database connection URI such as ```mongodb://root:root@localhost:27017/```, this will connect backend into the selected database for storing all persistent data but not including song files.


#todo see .env.example associated, link file

### Streaming with AWS SDK (STREAMING_SDK)

* **DISTRIBUTION_ID**: the id of the AWS Cloudfront distribution
* **MONGO_URI**: the database connection URI such as ```mongodb://root:root@localhost:27017/```, this will connect backend into the selected database for storing all persistent data but not including song files.


#todo see .env.example associated, link file

### No streaming with songs stored in database (DB_BLOB)


* **MONGO_URI**: the database connection URI such as ```mongodb://root:root@localhost:27017/```, this will connect backend into the selected database for storing all persistent including the song files.



#todo see .env.example associated, link file

----

## DEVELOPMENT READY ENVIROMENT

The following file can be used out of the box for development purpouse. It contains the following characteristics:

* **Local MongoDB database**. Use local MongoDB database, you can deploy one using our Docker stack as described [here](Docker.md).
* **Ready to use secret key**
* **DB_BLOB architecture selected**. This will only make necessary a MongoDB database because no cloud services are used in this architecture.
* **DEV** mode. It will enable hot reload for FastAPI.

```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
ENV_VALUE=DEV
ARCH=DB_BLOB
```


---

## ALL ROUND ENVIROMENT

You can also use the following `.env` file for changing between architectures as it contains all the variables needed. Just be sure to fill the the needed enviroments for the architecture seleted.


```
MONGO_URI=mongodb://root:root@localhost:27017/
SECRET_KEY_SIGN=f24e2f3ac557d487b6d879fb2d86f2b2
LAMBDA_URL=https://lambda-url.us-east-1.on.aws/path/
DISTRIBUTION_ID=A5K9R3X7Y2B8ZP
ENV_VALUE=DEV
ARCH=DB_BLOB
```