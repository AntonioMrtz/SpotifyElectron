# 1. Setup and run FRONTEND

In this section we will cover:

* How to setup the proyect
* Run the proyect and debug
* Run tests
* Package app for production

## 🛠 Setup the proyect

1. Enter frontend directory 

```
cd Electron;
```
2. Install the dependencies

```
npm install
```
3. Build the main and renderer process

```
npm run build
```
## ▶ Run the app in development mode

1. Run the app in hot reload debug mode 

```
npm start
```


## ✔️ Run tests

1. Go to Electron folder
```
cd Electron/;
```

2. Run tests

```
npm run test // run tests

or

npm run test:coverage // run tests and generate coverage in coverage folder
```

## ✔️ Linting

1. Run the linter
```
npm run lint
```


## ✏ Install the recommended extensions for VSCODE 

1. Go to extensions
2. Select filter extensions
3. Recommended
4. Workspace recommended
5. Install workspace recommended


## ✔️ Package app for production

1. Build the app

```
npm run build
```
2. Package the app for the current system and generate installer

```
npm run package
```
