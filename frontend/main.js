const { app, BrowserWindow, Tray, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;
let tray;

// Auto-install Python dependencies on first run
function installPythonDependencies() {
    return new Promise((resolve, reject) => {
        console.log('Installing Python dependencies...');
        const pipProcess = spawn('pip', ['install', '-r', 'requirements.txt']);
        
        pipProcess.stdout.on('data', (data) => {
            console.log(`pip: ${data}`);
        });
        
        pipProcess.stderr.on('data', (data) => {
            console.error(`pip error: ${data}`);
        });
        
        pipProcess.on('close', (code) => {
            if (code === 0) {
                console.log('Dependencies installed successfully');
                resolve();
            } else {
                reject(new Error(`pip install failed with code ${code}`));
            }
        });
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        frame: true,
        transparent: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
    
    
    // Hide instead of close
    mainWindow.on('close', (event) => {
        if (!app.isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
    });
}

function createTray() {
    tray = new Tray(path.join(__dirname, 'icon.png')); // You'll need to add an icon
    
    const contextMenu = Menu.buildFromTemplate([
        { label: 'Show Marvix', click: () => mainWindow.show() },
        { label: 'Hide', click: () => mainWindow.hide() },
        { type: 'separator' },
        { label: 'Quit', click: () => {
            app.isQuitting = true;
            app.quit();
        }}
    ]);
    
    tray.setToolTip('Marvix');
    tray.setContextMenu(contextMenu);
    
    tray.on('click', () => {
        mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
    });
}

function startPythonBackend() {
    pythonProcess = spawn('python', ['jarvis_backend.py']);
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });
}

// Auto-startup on boot
app.setLoginItemSettings({
    openAtLogin: true,
    openAsHidden: false
});

app.whenReady().then(async () => {
    try {
        await installPythonDependencies();
        startPythonBackend();
        createTray();
        setTimeout(createWindow, 2000); // Wait for Python to start
    } catch (error) {
        console.error('Setup failed:', error);
        // Create window anyway to show error
        createWindow();
    }
});

app.on('window-all-closed', () => {
    if (pythonProcess) pythonProcess.kill();
    app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
