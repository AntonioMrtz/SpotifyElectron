const { app, BrowserWindow, ipcMain,  net } = require('electron')

app.commandLine.appendSwitch('disable-features', 'OutOfBlinkCors')


const createWindow = () => {
    const win = new BrowserWindow({
        width: 1200,
        height: 800
    })

    win.loadFile('views/index.html')
}

app.whenReady().then(() => {
    createWindow()
})

ipcMain.handle("loadScripts", () => {


    const request = net.request("./views/sidebar.html");
    request.on("response", (response) => {

        console.log("golaaa")

    })

    request.end()

})