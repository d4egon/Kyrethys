@echo off
title Kyrethys - In Env (Keep This Open)

echo ================================================
echo   Kyrethys - Running inside Anaconda environment
echo   (this window stays open - watch for errors)
echo ================================================
echo.

set "Kyrethys_ROOT=C:\Kyrethys"
set "CONDA_PATH=%USERPROFILE%\Miniconda3\Scripts\activate.bat"

echo 1. Activating base environment...
call "%CONDA_PATH%" base
if errorlevel 1 (
    echo ERROR: Failed to activate base. Check path in script.
    pause
    exit /b 1
)
echo OK - base activated.

echo.
echo 2. Activating or creating Kyrethys-env...
conda env list | findstr /C:"Kyrethys-env" >nul
if errorlevel 1 (
    echo Creating Kyrethys-env with Python 3.12...
    conda create -n Kyrethys-env python=3.12 -y
    if errorlevel 1 (
        echo Failed to create env.
        pause
        exit /b 1
    )
)

call conda activate Kyrethys-env
if errorlevel 1 (
    echo Failed to activate Kyrethys-env.
    pause
    exit /b 1
)

echo OK - Kyrethys-env activated.
echo Python version:
python --version

echo.
echo 3. Installing/updating dependencies...
cd /d "%Kyrethys_ROOT%\backend"
pip install -r requirements.txt --quiet --upgrade

echo.
echo 4. Starting backend (Flask)...
start "Kyrethys - Backend" cmd /k "call %CONDA_PATH% base && conda activate Kyrethys-env && cd /d %Kyrethys_ROOT%\backend && title Kyrethys Backend && python jarvis_backend.py"

echo.
echo 5. Waiting 10 seconds for backend...
timeout /t 10 /nobreak >nul

echo.
echo 6. Starting frontend (Electron)...
cd /d "%Kyrethys_ROOT%\frontend"
npm start

echo.
echo ================================================
echo BOTH PARTS LAUNCHED!
echo - Backend in separate window
echo - Frontend UI should open now
echo Keep this window open for logs/errors.
pause