# Setup and run FRONTEND

In this section we will cover:

* How to setup the proyect
* Run the proyect and debug
* Run tests

## 🛠 Setup the proyect

### 1. Enter frontend folder

```
cd Electron
```
### 2. Install dependencies

```
npm install
```
### 3. Select architecture in global.ts
```
export const songArchitecture: SongArchitecture = SongArchitecture.STREAMING_ARCHITECTURE;
```

### 4. Build main and renderer process

```
npm run build
```

### 5. Run the project

```
npm start
```

## ▶ Select Music Player depending on Song Architecture backend ( optional )

You can select a custom music player dependending if the song architecture is managed by streaming or encoded base64 bytes. By default streaming service is selected.

### 1. Enter frontend global configuration file

```
cd Electron/src/global/global.ts
```

### 2. Select the music player architecture

We have to selected if we want . Backend should also have the same architecture selected in order for songs to be played correctly.

Files (RECOMMENDED for DEVELOPMENT)
```
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE
```
Streaming
```
export const songArchitecture: SongArchitecture = SongArchitecture.STREAMING_ARCHITECTURE
```

## ▶ Run the app in development mode

1. Run the app in hot reload debug mode

```
npm start
```


## 🧪 Run tests

1. Run tests

Normal run

```
npm run test
```
Run test and generate coverage

```
npm run test:coverage
```

## ✔️🎨 Linting and formatting

1. Run lint check and format. This will force fix any error that has no impact and can be solved automatically
```
npm run lint
```

## 🎨 Style

1. Run the style check
```
npm run format:check
```

2. Run the style formatter
```
npm run format:format
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
npm run package --win --mac --linux
```
