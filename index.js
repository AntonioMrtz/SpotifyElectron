const { app, BrowserWindow, ipcMain, net } = require('electron')

const path = require('path')

app.commandLine.appendSwitch('disable-features', 'OutOfBlinkCors')


const createWindow = () => {
    const win = new BrowserWindow({
        width: 1200,
        height: 800, webPreferences: {
            nodeIntegration: false, // is default value after Electron v5
            contextIsolation: true, // protect against prototype pollution
            enableRemoteModule: false, // turn off remote
            webviewTag: true,
            preload: path.join(__dirname, "preload.js") // use a preload script
        }
    })

    win.loadFile('views/index.html')
}

app.whenReady().then(() => {
    createWindow()
})

ipcMain.handle("loadScripts", () => {


    /* const request = net.request("./views/sidebar.html");
    request.on("response", (response) => {

        console.log("golaaa")

    })

    request.end() */

    console.log("dentro handler")

})