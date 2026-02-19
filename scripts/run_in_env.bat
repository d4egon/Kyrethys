@echo off
title Marvix - In Env (Keep This Open)

echo ================================================
echo   Marvix - Running inside Anaconda environment
echo   (this window stays open - watch for errors)
echo ================================================
echo.

echo 1. Activating base environment...
call "C:\Users\hansa\Miniconda3\Scripts\activate.bat" base
if errorlevel 1 (
    echo ERROR: Failed to activate base. Check path.
    pause
    exit /b 1
)
echo OK - base activated.

echo.
echo 2. Activating or creating marvix-env...
conda env list | findstr /C:"marvix-env" >nul
if errorlevel 1 (
    echo Creating marvix-env with Python 3.12...
    conda create -n marvix-env python=3.12 -y
    if errorlevel 1 (
        echo Failed to create env.
        pause
        exit /b 1
    )
)

call conda activate marvix-env
if errorlevel 1 (
    echo Failed to activate marvix-env.
    pause
    exit /b 1
)

echo OK - marvix-env activated.
echo Python version:
python --version

echo.
echo 3. Installing/updating dependencies...
pip install -r requirements.txt --quiet --upgrade

echo.
echo 4. Starting backend (Flask)...
start "Marvix - Backend" cmd /k "title Marvix Backend && python jarvis_backend.py"

echo.
echo 5. Waiting 10 seconds for backend...
timeout /t 10 /nobreak >nul

echo.
echo 6. Starting frontend (Electron)...
npm start

echo.
echo ================================================
echo BOTH PARTS LAUNCHED!
echo - Backend in separate window
echo - Frontend UI should open now
echo Keep this window open for logs/errors.
pause