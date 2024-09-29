# Setup and run FRONTEND

In this section we will cover:

- How to setup the proyect
- Run the proyect and debug
- Run tests

## 🛠 Setup the proyect

### 1. Enter frontend folder

```console
cd Electron
```

### 2. Install dependencies

```console
npm install
```

### 3. Select architecture in global.ts

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.BLOB_ARCHITECTURE;
```

### 4. Build main and renderer process

```console
npm run build
```

### 5. Run the project

```console
npm start
```

## ▶ Select Music Player depending on Song Architecture backend ( optional )

You can select a custom music player dependending if the song architecture is managed by regular or serverless streaming. By default `BLOB` architecture service is selected.

### 1. Enter frontend global configuration file

```
cd Electron/src/global/global.ts
```

### 2. Select the music player architecture

We have to selected if we want. Backend should also have the same architecture selected in order for songs to be played correctly.

Blob (PRODUCTION and DEVELOPMENT)

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.BLOB_ARCHITECTURE
```

Streaming (deprecated)

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.SERVERLESS_ARCHITECTURE
```

## ▶ Run the app in development mode

1. Run the app in hot reload debug mode

```console
npm start
```
