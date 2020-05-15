const {dialog, ipcMain} = require("electron");

function IpcList(argMainWindow, argChildWindow)
{
    let mainWindow = argMainWindow;
    let childWindow = argChildWindow;

    // Check if renderers finished loading
    mainWindow.webContents.on("did-finish-load", () => {
        childWindow.webContents.on("did-finish-load", () =>{
            console.log("MAIN AND CHILD RENDERERS FINISHED LOADING!")
        });
    });
    
    // MESSAGE TO MAIN RENDERER
    let send_main = (message) => {
        mainWindow.webContents.send('MESSAGE_FROM_SUB', message)
        console.log("IPC_MAIN: MESSAGE SENT TO MAIN RENDERER")
     }
    
    // MAIN_RENDERER
    ipcMain.on("MAIN_RENDERER_READY", () => {
        console.log("MAIN RENDERER: RENDERER IS READY");
    });
    ipcMain.on("MAIN_RENDERER_SEND", (event, data) => {
        console.log("MAIN_RENDERER: MESSAGE RECEIVED");
        if(data.execute)
        {
            childWindow.webContents.send("COMMAND_FROM_MAIN", data);
            console.log("MAIN_RENDERER: MESSAGE SENT TO SUB RENDERER");
            event.reply("REPLY", "MESSAGE IS BEING PROCEED");
        }
    });

    // Select path
    ipcMain.on("SELECT_PATH", async (event,arg) => {
        const result = await dialog.showOpenDialog(mainWindow, {
            properties: ['openDirectory']
        })
        event.reply("PATH_REPLY", result.filePaths)
    })

    // SUB_RENDERER
    ipcMain.on("SUB_RENDERER_READY", () => {
        console.log("SUB_RENDERER: RENDERER IS READY");
    });
    ipcMain.on("SUB_RENDERER_SEND", (event, data) => {
        console.log('SUB_RENDERER: MESSAGE RECEIVED');
        console.log(data);
        if(data.hasOwnProperty('reply'))
            send_main(data);
    });
    ipcMain.on("SUB_RENDERER_LOG", (event,args) => {
       console.log("SUB_RENDERER: " + args);
    });

    // READ AND SEND BACK CONFIGURATION
    ipcMain.on("READ_CONFIG", (event, args) => {
        childWindow.webContents.send("READ_CONFIG")
    });
    ipcMain.on("SEND_CONFIG", (event, args) => {
        console.log("SUB_RENDERER: CONFIG RECEIVED")
        console.log(args)
        mainWindow.webContents.send("SEND_CONFIG", args);
    })
}

module.exports = IpcList;