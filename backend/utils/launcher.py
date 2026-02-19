import os

# Fallback-liste (udvid efter behov)
FALLBACK_PATHS = {
    "spotify": r"%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\Spotify.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "paint": "mspaint.exe",
    "wordpad": "wordpad.exe",
    "explorer": "explorer.exe",
    "taskmgr": "taskmgr.exe",
    "chrome": r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe",
    "firefox": r"%PROGRAMFILES%\Mozilla Firefox\firefox.exe",
    "edge": "msedge.exe",
    "steam": r"%PROGRAMFILES(x86)%\Steam\steam.exe",
    "discord": r"%LOCALAPPDATA%\Discord\app-*\Discord.exe",
    "vlc": r"%PROGRAMFILES%\VideoLAN\VLC\vlc.exe",
    "zoom": r"%APPDATA%\Zoom\bin\Zoom.exe",
    "teams": r"%LOCALAPPDATA%\Microsoft\Teams\current\Teams.exe",
    "code": r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
}

def launch_app(app_name, app_paths):
    if not app_name:
        return "Intet app-navn angivet"

    app_key = app_name.lower().strip()

    # 1. Præcist match i JSON
    if app_key in app_paths:
        exe_path = os.path.expandvars(app_paths[app_key])
        exe_path = os.path.normpath(exe_path)
        if os.path.exists(exe_path):
            try:
                os.startfile(exe_path)
                print(f"JSON hit: {exe_path}")
                return f"Åbner {app_name} fra JSON!"
            except Exception as e:
                print(f"JSON fejl: {e}")

    # 2. Fallback-liste
    if app_key in FALLBACK_PATHS:
        exe_path = os.path.expandvars(FALLBACK_PATHS[app_key])
        exe_path = os.path.normpath(exe_path)
        if os.path.exists(exe_path):
            try:
                os.startfile(exe_path)
                print(f"Fallback hit: {exe_path}")
                return f"Åbner {app_name} fra fallback!"
            except Exception as e:
                print(f"Fallback fejl: {e}")

    # 3. Direkte
    try:
        os.startfile(app_key)
        print(f"Direkte: {app_key}")
        return f"Prøver direkte: {app_name}"
    except Exception as e:
        print(f"Direkte fejl: {e}")
        return f"Kunne ikke åbne '{app_name}'"