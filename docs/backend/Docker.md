# Docker

Docker is used primarily in the project for:

- **Easing development** automating the set up process for infrastructure like databases and other utilities. The aim was to give a simple script so the developers can focus on getting the work done and to trying to deploy the project or messing installing and configuring different services.
- **Easing the production development**. When it comes to deploying the app into production is handy to have a script that allows the app to run in every system containerized with a single command. When deploying multiple instances of the backend the deployment time will be cut significantly.

Its recommended to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed but only having docker will work.

## Stacks

Currently the app has two stacks, one for development and one for deploying into production. All Docker related scripts and configuration is donde under the `docker/` folder.

### Development

The stack contains the following:

- MongoDB Database
- Mongo Express administration dashboard
  - Connect [http://localhost:8081/](http://localhost:8081/)
  - User: admin & password: pass
- Backend Server (Stop the container if you're deploying the backend server locally)

This stack contains all you need to develop locally on your device. It's recommended to be used paired with the `BLOB ARCHITECTURE` architecture so you only need a mongoDB database to make the app work. See [architectures](Architecture.md) for more info on what services has to be deployed depending on the architecture selected.

Mongo Express administration dashboard is also shipped using this stack. This service wil let you administrate the items in the Database graphically. More info on the [official image](https://hub.docker.com/_/mongo-express).

Run this command to build and up the development containers:

```
./build_and_up_dev.sh
```

### Production

This stack only contains backend server and its aimed to fast deployment into production of the service. Its recommended to use a remote database for production mode.

Run the stack with:

```
./build_and_up_prod.sh
```
