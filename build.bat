@echo off
REM ============================================================
REM  build.bat — بناء ملف exe لنظام إدارة المخازن
REM  Developer: AMR ABDELRAZK
REM ============================================================
chcp 65001 >nul
setlocal

REM ─── مسارات ───
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "PYTHON_BIN=C:\Users\we\AppData\Local\Python\bin\python.exe"
if not exist "%PYTHON_BIN%" (
    echo [ERROR] Python not found at: %PYTHON_BIN%
    echo [INFO]  Edit build.bat and set PYTHON_BIN to your Python path.
    pause
    exit /b 1
)

REM ─── التحقق من PyInstaller ───
"%PYTHON_BIN%" -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found — installing...
    "%PYTHON_BIN%" -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM ─── تحقق من المكتبات ───
echo [CHECK] Verifying required libraries...
"%PYTHON_BIN%" -c "import sqlalchemy, openpyxl, reportlab, arabic_reshaper, bidi; print('[OK] All libraries present')"
if errorlevel 1 (
    echo [ERROR] Missing libraries. Run:
    echo         pip install -r requirements.txt
    pause
    exit /b 1
)

REM ─── تنظيف builds السابقة ───
echo [CLEAN] Removing old build/dist...
if exist "build"  rmdir /s /q "build"
if exist "dist"   rmdir /s /q "dist"

REM ─── بناء ───
echo.
echo [BUILD] Building exe with PyInstaller (this may take 2-4 minutes)...
"%PYTHON_BIN%" -m PyInstaller build.spec --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller failed.
    pause
    exit /b 1
)

REM ─── نسخ مجلد data (المستخدم يحتاج ملفاته) ───
echo [COPY] Preparing data folder next to exe...
if exist "dist\WarehouseSystem\data" (
    echo       data folder already exists — keeping existing.
) else (
    mkdir "dist\WarehouseSystem\data"
    mkdir "dist\WarehouseSystem\data\attachments"
    mkdir "dist\WarehouseSystem\data\backups"
    echo       created empty data folder.
)

REM ─── نسخ README ───
if exist "README.md" copy /y "README.md" "dist\WarehouseSystem\" >nul

REM ─── إنهاء ───
echo.
echo ============================================================
echo [SUCCESS] Build complete!
echo.
echo   EXE folder:  %PROJECT_DIR%dist\WarehouseSystem\
echo   Executable:  %PROJECT_DIR%dist\WarehouseSystem\WarehouseSystem.exe
echo ============================================================
echo.
pause
endlocal