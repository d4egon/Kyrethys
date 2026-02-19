import os
import json
from tqdm import tqdm  # progress bar

# Almindelige mapper at scanne
directories = [
    os.path.expandvars('%ProgramFiles%'),
    os.path.expandvars('%ProgramFiles(x86)%'),
    os.path.expandvars('%APPDATA%'),
    os.path.expandvars('%LOCALAPPDATA%'),
    os.path.expandvars('%USERPROFILE%\\Desktop'),
    os.path.expandvars('%USERPROFILE%\\Downloads'),
]

exe_paths = {}

# Saml alle filer først for at vise progress
all_files = []
for dir_path in directories:
    if not os.path.exists(dir_path):
        continue
    for root, _, files in os.walk(dir_path):
        all_files.extend((os.path.join(root, f), f) for f in files)

# Progress bar over alle filer
with tqdm(total=len(all_files), desc="Scanning .exe files") as pbar:
    for full_path, file in all_files:
        pbar.update(1)
        if file.lower().endswith('.exe'):
            # Kun tilføj hvis det ser "rimeligt" ud (filtrér støj)
            app_name = os.path.splitext(file)[0].lower()
            if len(app_name) > 3 and not app_name.startswith(('unins', 'setup', 'install', '$')):
                placeholder_path = full_path.replace(os.path.expanduser('~'), '%USERPROFILE%').replace('\\', '/')
                if app_name not in exe_paths:  # behold første/første fundne
                    exe_paths[app_name] = placeholder_path

# Skriv til JSON
with open('app_paths.json', 'w') as f:
    json.dump(exe_paths, f, indent=4)

print(f"\nFærdig! app_paths.json oprettet med {len(exe_paths)} apps.")
print("Eksempel (første 5):", dict(list(exe_paths.items())[:5]))