@echo off

echo Cleaning...
rmdir /S /Q build 2>nul
rmdir /S /Q dist 2>nul

echo Building HugoStudio...
pyinstaller ^
    --windowed ^
    --name HugoStudio ^
    --add-data "resources;resources" ^
    --add-data "docs;docs" ^
    main.py

echo.
echo Build complete.
pause