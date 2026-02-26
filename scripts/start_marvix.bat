@echo off
title Kyrethys Launcher - Simple Start
color 0A
cls

echo ================================================
echo   Kyrethys Launcher
echo ================================================
echo.

set "Kyrethys_ROOT=C:\Kyrethys"
set "CONDA_PATH=%USERPROFILE%\Miniconda3\Scripts\activate.bat"

echo Opening Anaconda Prompt and running Kyrethys...
start "Kyrethys - In Env" /D "%Kyrethys_ROOT%\scripts" cmd /k "run_in_env.bat"

echo.
echo Done. Look for the new window titled "Kyrethys - In Env".
echo It will stay open and show every step.
pause