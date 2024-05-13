@echo off

cd %~dp0

call ".\env\Scripts\activate"

python mods_updater.py

if errorlevel 1 pause

@REM start "" "%PATH_7D2D%\7DaysToDie.exe"