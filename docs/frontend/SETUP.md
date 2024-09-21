# Setup and run FRONTEND

In this section we will cover:

- How to setup the proyect
- Run the proyect and debug
- Run tests

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
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE;
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

You can select a custom music player dependending if the song architecture is managed by streaming or encoded base64 bytes. By default file architecture service is selected.

### 1. Enter frontend global configuration file

```
cd Electron/src/global/global.ts
```

### 2. Select the music player architecture

We have to selected if we want . Backend should also have the same architecture selected in order for songs to be played correctly.

Files (DEVELOPMENT and PRODUCTION)

```
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE
```

Streaming (deprecated)

```
export const songArchitecture: SongArchitecture = SongArchitecture.STREAMING_ARCHITECTURE
```

## ▶ Run the app in development mode

1. Run the app in hot reload debug mode

```
npm start
```
