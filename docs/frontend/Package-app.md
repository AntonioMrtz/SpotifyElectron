## 📦 Package app

In this section we will cover how to package app for production. After following the steps the generated installer will be placed at `Electron/release/build`.

### 1. Select wanted architecture in global.ts

```
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE;
```

### 2. Build the app

```
npm run build
```

### 3. Package the app for the current system (or all platforms) and generate installer

Packaging for all platforms

```
npm run package --win --mac --linux
```

Packaging for the current platform

```
npm run package
```
