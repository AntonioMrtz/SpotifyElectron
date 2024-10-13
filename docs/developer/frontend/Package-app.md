# 📦 Package app

In this section we will cover how to package app for production. After following the steps the generated installer will be placed at `Electron/release/build`.

## 1. Update `global.ts` client data

```ts
export const songArchitecture: SongArchitecture = SongArchitecture.BLOB_ARCHITECTURE;
```

### Update production backend url

❗ Set backend url path without trailing `/`

```ts
export const backendBaseUrl: string = 'http://127.0.0.1:8000';
```

## 2. Build the app

```console
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

#### Windows

An `.exe` will be generated

```console
npm run package:win
```

##### Deb (not working)

```console
npm run package:linux:deb
```
