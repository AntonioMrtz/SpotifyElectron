const { app,contextBridge ,BrowserWindow, ipcRenderer } = require('electron')


let homeBridge = {

    loadScripts : async () => {

        await ipcRenderer.invoke("loadScripts");
    },
    func2 : () => {

        
    }



}

contextBridge.exposeInMainWorld("homeBridge",homeBridge)