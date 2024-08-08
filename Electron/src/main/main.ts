/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import path from 'path';
import { app, BrowserWindow, shell, ipcMain, clipboard, Data } from 'electron';
import Global from 'global/global';
import { resolveHtmlPath } from './util';

let mainWindow: BrowserWindow | null = null;

/* Events */

ipcMain.on('toogle-fullscreen', async () => {
  if (mainWindow && mainWindow.isFullScreen()) mainWindow.setFullScreen(false);
  else if (mainWindow) mainWindow.setFullScreen(true);
});

ipcMain.handle('copy-to-clipboard', async (event, dataToClipboard) => {
  const data: Data = {};
  // eslint-disable-next-line prefer-destructuring
  data.text = dataToClipboard;

  clipboard.write(data);
});

ipcMain.handle('load-previous-url', async () => {
  mainWindow?.webContents.goBack();
});

ipcMain.handle('load-forward-url', async () => {
  mainWindow?.webContents.goForward();
});

ipcMain.handle('handle-url-change', async () => {
  const eventResponse: Global.HandleUrlChangeResponse = {
    canGoBack: mainWindow?.webContents.canGoBack(),
    canGoForward: mainWindow?.webContents.canGoForward(),
  };

  return eventResponse;
});

/* Settings */

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

if (isDebug) {
  require('electron-debug')();
}

const installExtensions = async () => {
  const installer = require('electron-devtools-installer');
  const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
  const extensions = ['REACT_DEVELOPER_TOOLS'];

  return installer
    .default(
      extensions.map((name) => installer[name]),
      forceDownload,
    )
    .catch(console.log);
};

const createWindow = async () => {
  if (isDebug) {
    await installExtensions();
  }

  const RESOURCES_PATH = app.isPackaged
    ? path.join(process.resourcesPath, 'assets')
    : path.join(__dirname, '../../assets');

  /* const getAssetPath = (...paths: string[]): string => {
    return path.join(RESOURCES_PATH, ...paths);
  }; */

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 730,
    icon: path.join(RESOURCES_PATH, '/icon.ico'),
    webPreferences: {
      preload: app.isPackaged
        ? path.join(__dirname, 'preload.js')
        : path.join(__dirname, '../../.erb/dll/preload.js'),
    },
  });

  mainWindow.setMenuBarVisibility(false);
  mainWindow.loadURL(resolveHtmlPath('index.html'));

  mainWindow.on('ready-to-show', () => {
    if (!mainWindow) {
      throw new Error('"mainWindow" is not defined');
    }
    const ses = mainWindow.webContents.session;

    // Interceptamos las solicitudes web
    ses.webRequest.onBeforeSendHeaders(async (details, callback) => {
      // Add credentials to all requests
      try {
        const cookies = await ses.cookies.get({});

        const filteredJwtTokens = cookies.filter((cookie) => {
          return cookie.name === 'jwt';
        });

        if (filteredJwtTokens && filteredJwtTokens[0]) {
          details.requestHeaders.Authorization =
            filteredJwtTokens[filteredJwtTokens.length - 1].value;
        }

        callback({ cancel: false, requestHeaders: details.requestHeaders });
      } catch (error) {
        console.error('Error getting cookies:', error);
        callback({ cancel: false, requestHeaders: details.requestHeaders });
      }
    });

    if (process.env.START_MINIMIZED) {
      mainWindow.minimize();
    } else {
      mainWindow.show();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Open urls in the user's browser
  mainWindow.webContents.setWindowOpenHandler((edata) => {
    shell.openExternal(edata.url);
    return { action: 'deny' };
  });
};

/**
 * Add event listeners...
 */

app.on('window-all-closed', () => {
  // Respect the OSX convention of having the application in memory even
  // after all windows have been closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app
  .whenReady()
  .then(() => {
    createWindow();
    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (mainWindow === null) createWindow();
    });
  })
  .catch(console.log);
