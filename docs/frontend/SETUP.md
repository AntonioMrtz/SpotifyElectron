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
3. Select wanted architecture by going to global.ts
```
export const songArchitecture: SongArchitecture = SongArchitecture.STREAMING_ARCHITECTURE;
```

4. Build the main and renderer process

```
npm run build
```

5. Run the project

```
npm start
```

## ▶ Select Music Player depending on Song Architecture backend ( optional )

You can select a custom music player dependending if the song architecture is managed by streaming or encoded base64 bytes. By default streaming service is selected.

1. Enter frontend global configuration file 

```
cd Electron/src/global/global.ts;
```

2. Select the architecture

```
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE or SongArchitecture.STREAMING_ARCHITECTURE;
```

## ▶ Run the app in development mode

1. Run the app in hot reload debug mode 

```
npm start
```


## ✔️ Run tests

1. Run tests

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

1. Select wanted architecture by going to global.ts
```
export const songArchitecture: SongArchitecture = SongArchitecture.STREAMING_ARCHITECTURE;
```

2. Build the app

```
npm run build
```
3. Package the app for the current system and generate installer

```
npm run package
```
