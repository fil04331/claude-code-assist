@echo off
REM Setup script for Quebec Market Trends MVP (Windows)

echo ===========================================================
echo Quebec Market Trends - Setup Script (Windows)
echo ===========================================================
echo.

REM Check Python
echo Checking Python installation...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo √ %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv\" (
    echo   Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo √ Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo √ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo √ pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
echo √ Dependencies installed
echo.

REM Create directories
echo Creating directories...
if not exist "data\" mkdir data
if not exist "logs\" mkdir logs
if not exist "data\backups\" mkdir data\backups
echo √ Directories created
echo.

REM Copy environment file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env >nul
    echo √ .env file created
) else (
    echo   .env file already exists, skipping...
)
echo.

echo ===========================================================
echo √ Setup complete!
echo ===========================================================
echo.
echo Next steps:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Collect initial data (5-10 minutes):
echo      python run_collection.py
echo.
echo   3. Launch the dashboard:
echo      python run_dashboard.py
echo.
echo For more information, see QUICKSTART.md or docs\README_MVP.md
echo.
pause
