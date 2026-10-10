@echo off
setlocal
cd /d "%~dp0"
title MAHFOOZ Restaurant
color 06
echo ============================================
echo       MAHFOOZ RESTAURANT WEBSITE
echo ============================================
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% --version
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer from python.org and enable Add Python to PATH.
  pause
  exit /b 1
)
echo Installing required packages...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo Package installation failed. Check your internet connection and Python installation.
  pause
  exit /b 1
)
echo Starting MAHFOOZ...
echo Website: http://127.0.0.1:5000
echo Admin:   http://127.0.0.1:5000/admin/login
echo Local demo login: admin / admin123
%PY% app.py
if errorlevel 1 (
  echo The server stopped because of an error. Copy the complete error text to troubleshoot it.
)
pause
