# Docker

Docker is used primarily in the project for:

- **Easing development** automating the set up process for infrastructure like databases and other utilities. The aim was to give a simple script so the developers can focus on getting the work done and to trying to deploy the project or messing installing and configuring different services.
- **Easing the production development**. When it comes to deploying the app into production is handy to have a script that allows the app to run in every system containerized with a single command. When deploying multiple instances of the backend the deployment time will be cut significantly.

it's recommended to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed but only having `docker` and `docker compose` will work.

## Stacks

Currently the app has two types of stack, one for development and one for deploying into production. All Docker related scripts and configuration is donde under the `docker/` folder.

### Development

This stack uses `docker/env/dev.env`.

Mongo Express administration dashboard is also shipped using this stack. This service wil let you administrate the items in the Database graphically. More info on the [official image](https://hub.docker.com/_/mongo-express).

#### For Backend

Launches all Backend dependencies needed by the Backend app runned locally for development

- MongoDB Database
- Mongo Express administration dashboard
  - Connect [http://localhost:8081/](http://localhost:8081/)
  - User: admin & password: pass

```console
./build_and_up_dev_backend.sh
```

#### For frontend

Launches Backend and its dependencies for Frontend local development

- Backend app
- MongoDB Database
- Mongo Express administration dashboard
  - Connect [http://localhost:8081/](http://localhost:8081/)
  - User: admin & password: pass

```console
./build_and_up_dev_standalone.sh
```

### Production

This stack contains the following services configured for production:

- Backend app
- MongoDB database

`Backend/docker/env/prod.env` is used by the stack and requires to introduce production environment variables. See [Production environment](Environment.md) for more info.

Run the stack with:

```console
./build_and_up_prod.sh
```
