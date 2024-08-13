/* eslint import/prefer-default-export: off */
import { URL } from 'url';
import path from 'path';
import { BrowserWindow } from 'electron';

export function resolveHtmlPath(htmlFileName: string) {
  if (process.env.NODE_ENV === 'development') {
    const port = process.env.PORT || 1212;
    const url = new URL(`http://localhost:${port}`);
    url.pathname = htmlFileName;
    return url.href;
  }
  return `file://${path.resolve(__dirname, '../renderer/', htmlFileName)}`;
}

/* Intercept request headers and insert cookies. It has to be called after `ready-to-show` event */
export const interceptRequestHeaders = (mainWindow: BrowserWindow) => {
  if (!mainWindow) return;
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
};
