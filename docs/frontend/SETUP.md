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

### 3. Build main and renderer process

```console
npm run build
```

### 4. Run the app

#### Standar

```console
npm start
```

#### Debug (**Chromium based browser is needed**)

1. Launch VSCODE debug script `Electron: All`
2. Launch browser: `chromium --remote-debugging-port=9223 --user-data-dir=remote-debug-profile`. Replace `chromium` with the path of your browser executable
3. Go to `localhost:1212` on the launched chromium based browser
4. Refresh using F5 until the program stops at the selected breakpoint (this may require multiple refreshes).


## ▶ Select Music Player based on Song Architecture backend (optional)

You can select a custom music player dependending if the song architecture is managed by regular or serverless streaming. By default `BLOB` architecture service is selected.

### 1. Enter frontend global configuration file

```
cd Electron/src/global/global.ts
```

### 2. Select the music player streaming architecture

We have to selected if we want. Backend should also have the same architecture selected in order for songs to be played correctly.

#### BLOB (PRODUCTION and DEVELOPMENT)

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.BLOB_ARCHITECTURE
```

#### Serverless (deprecated)

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.SERVERLESS_ARCHITECTURE
```