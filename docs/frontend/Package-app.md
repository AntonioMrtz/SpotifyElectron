# 📦 Package app

In this section we will cover how to package app for production. After following the steps the generated installer will be placed at `Electron/release/build`.

## 1. Select wanted architecture in global.ts

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.FILE_ARCHITECTURE;
```

## 2. Build the app
console
```
npm run build
```

## 3. Package the app

* Packaging for MacOS can be only done from a native system
* From linux you can package the app for `AppImage` and `deb` format, and Windows if `wine` is installed


### Native host

Packages app for native system format

```console
npm run package
```

### Linux host

#### AppImage

```console
npm run package:linux:appimage
```

An `.AppImage` file will be generated. If there's any error while trying to open the app try this:

```console
sudo apt install libfuse2 &&
cd release/build/ &&
chmod 777 {generated-app-name}.AppImage &&
./{generated-app-name}.AppImage --no-sandbox
```

#### Windows

An `.exe` will be generated

```console
npm run package:win
```

##### Deb (not working)

```console
npm run package:linux:deb
```
