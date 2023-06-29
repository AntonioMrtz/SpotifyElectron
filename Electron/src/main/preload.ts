// Disable no-unused-vars, broken for spread args
/* eslint no-unused-vars: off */
import { contextBridge, ipcRenderer, IpcRendererEvent } from 'electron';

export type ChannelToogleFullScreen = 'toogle-fullscreen';
export type ChannelSubmitSong = 'submit-song';



const electronHandler = {
  /* submitSong: {
    sendMessage(channel: ChannelSubmitSong, ...args: unknown[]) {
      ipcRenderer.send(channel, ...args);
    },
  }, */
  toogleFullScreen : {
    sendMessage(channel: ChannelToogleFullScreen, ...args: unknown[]) {
      ipcRenderer.send(channel, ...args);
    },
  }
};

contextBridge.exposeInMainWorld('electron', electronHandler);

export type ElectronHandler = typeof electronHandler;


/* const electronHandler = {
  ipcRenderer: {
    sendMessage(channel: ChannelToogleFullScreen, ...args: unknown[]) {
      ipcRenderer.send(channel, ...args);
    },
    on(channel: ChannelToogleFullScreen, func: (...args: unknown[]) => void) {
      const subscription = (_event: IpcRendererEvent, ...args: unknown[]) =>
        func(...args);
      ipcRenderer.on(channel, subscription);

      return () => {
        ipcRenderer.removeListener(channel, subscription);
      };
    },
    once(channel: ChannelToogleFullScreen, func: (...args: unknown[]) => void) {
      ipcRenderer.once(channel, (_event, ...args) => func(...args));
    },
  },
}; */
