const { app, BrowserWindow, ipcMain, net } = require('electron')
const isDev = require('electron-is-dev');

const path = require('path')

app.commandLine.appendSwitch('disable-features', 'OutOfBlinkCors')


const createWindow = () => {

    
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth:800,
        minHeight: 600,
        icon:"",
        webPreferences: {
            nodeIntegration: false, // is default value after Electron v5
            contextIsolation: true, // protect against prototype pollution
            enableRemoteModule: false, // turn off remote
            webviewTag: true,
            preload: path.join(__dirname, "preload.js") // use a preload script
        },
        
    })

    win.maximize();

    //win.loadFile('spotify-electron/public/index.html')
    win.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '../build/index.html')}`);
    win.setMenuBarVisibility(false);
    //win.setIcon("./favicon.ico")
    if (isDev) {
      win.webContents.openDevTools();
    }
    
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