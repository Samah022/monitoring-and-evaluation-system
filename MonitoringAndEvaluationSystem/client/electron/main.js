
const { BrowserWindow, app } = require('electron');
const path = require('path');

// const isDev = !app.isPackaged;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: "white",
    webPreferences: {
      nodeIntegration: false,
      worldSafeExecuteJavaScript: true,
      contextIsolation: true,
    //   preload: path.join(__dirname, 'preload.js')
    }
  })

//   win.loadFile('..//public//index.html'); // the main html page link
  win.loadFile(path.join(__dirname, '..','/public/index.html'));
  win.loadURL("http://localhost:3000")


}

// require('electron-reload')(__dirname, {
// electron: path.join(__dirname,'..' ,'node_modules', '.bin', 'electron')
// })


app.whenReady().then(createWindow)