@echo off
setlocal EnableDelayedExpansion

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Run PIP-MAN
python pip_manager.py

:: Deactivate the virtual environment when done
deactivate