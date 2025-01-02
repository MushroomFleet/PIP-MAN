@echo off
setlocal EnableDelayedExpansion

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete!
echo To run PIP-MAN, use run-pipman.bat
pause