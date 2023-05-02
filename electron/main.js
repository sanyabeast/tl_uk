const { app, BrowserWindow, ipcMain } = require('electron');
const express = require('express');
const path = require('path');
const http = require('http');

let win = null

function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadURL('https://translate.google.com/?sl=ru&tl=uk');
    win.openDevTools()
}

app.whenReady().then(() => {
    // Create Express App
    const expressApp = express();

    expressApp.use(express.json()); // add this line to use body-parser as middleware
    expressApp.use(express.static(path.join(__dirname, 'public')));

    expressApp.post('/translate', async (req, res) => {
        translation = await get_translation(req.body)
        // Your translation logic goes here
        // For now, just send back the received data
        res.json({ translation });
    });

    // Start Express server
    const server = http.createServer(expressApp);
    server.listen(1338, () => {
        console.log('Server started on http://localhost:1338');

        // Only create the Electron window after the server has started
        createWindow();
    });

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});

function get_translation(params) {
    return new Promise((resolve, reject) => {
        ipcMain.once('get_translation.response', (event, data) => {
            resolve(data.translation)
        })

        win.webContents.send('get_translation', params)
    })
}