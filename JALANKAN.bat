@echo off
chcp 65001 >nul
title Generator Foto 3x4 ke PDF

echo ============================================================
echo           GENERATOR FOTO 3x4 KE PDF
echo ============================================================
echo.

set /p FOLDER_FOTO="Masukkan path folder foto: "

echo.
echo [*] Memproses folder: %FOLDER_FOTO%
echo.

"C:\Users\Nama_File\AppData\Local\Programs\Python\Python314\python.exe" "%~dp0foto.py" "%FOLDER_FOTO%" (file python anda)

echo.
pause
