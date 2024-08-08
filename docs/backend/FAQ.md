# FAQ

## ◾ Database connection failed, stopping server

When launching the backend app, the following errors may appear 5 seconds after the application starts:

* `SystemExit: Database connection failed, stopping server`
* `CRITICAL - Error establishing connection with database: Ping to the database failed`

Both errors indicate a failure to connect to the database. To diagnose the issue:

1. Verify if your database is active by navigating to `localhost:27017` in your browser (the address might vary based on your database setup; `localhost:27017` is typical for development).
2. If a blank page appears with the message: `It looks like you are trying to access MongoDB over HTTP on the native driver port.`
then the database is running correctly.
3. If nothing appears, revisit the Docker deployment steps to ensure everything was completed properly.

`It looks like you are trying to access MongoDB over HTTP on the native driver port.`

If nothing appears, check that the steps provided in [Docker deployment](Docker.md) were completed correctly.

## ◾ Docker build scripts cannot be run

If you cannot run Docker scripts or they fail while executing:

1. Ensure you have a valid `.env` file by following the guidelines provided in the [Environment guide](Enviroment.md).
2. `/bin/bash^M: bad interpreter: No such file or directory`. This indicates a problem with return carriages; Linux represents them differently. Try running `sed -i -e 's/\r$//' script-name.sh` to convert Windows format to Linux.

## ◾ '_PropertiesManager' object has no attribute 'ENV_VALUE'

If you encounter an error similar to:

`AttributeError: '_PropertiesManager' object has no attribute 'ENV_VALUE'`

The environments are not being passed correctly to the app. Ensure you follow the [Environment guide](Enviroment.md) correctly and provide the required environments in a `.env` file under the Backend directory. If the error persists, restarting VS Code sometimes helps when environment variables are not loaded.

## ◾ I can't authenticate in backend Swagger docs

There's a detailed guide about login and authentication [here](../Auth-Login.md).
