// Disable no-unused-vars, broken for spread args
/* eslint no-unused-vars: off */
import { contextBridge, ipcRenderer } from 'electron';

export type ChannelToogleFullScreen = 'toogle-fullscreen';
export type ChannelCopyToClipboard = 'copy-to-clipboard';
export type ChannelLoadPreviousUrl = 'load-previous-url';
export type ChannelLoadForwardUrl = 'load-forward-url';
export type ChannelHandleUrlChange = 'handle-url-change';

const electronHandler = {
  toogleFullScreen: {
    sendMessage(channel: ChannelToogleFullScreen) {
      ipcRenderer.send(channel);
    },
  },

  copyToClipboard: {
    sendMessage(channel: ChannelCopyToClipboard, dataToClipboard: string) {
      ipcRenderer.invoke(channel, dataToClipboard);
    },
  },

  loadPreviousUrl: {
    sendMessage(channel: ChannelLoadPreviousUrl) {
      ipcRenderer.invoke(channel);
    },
  },

  loadForwardUrl: {
    sendMessage(channel: ChannelLoadForwardUrl) {
      ipcRenderer.invoke(channel);
    },
  },

  handleUrlChange: {
    sendMessage(channel: ChannelHandleUrlChange) {
      return ipcRenderer.invoke(channel);
    },
  },
};

contextBridge.exposeInMainWorld('electron', electronHandler);

export type ElectronHandler = typeof electronHandler;
