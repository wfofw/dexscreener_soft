@echo off
chcp 65001 >nul
<<<<<<< HEAD
=======
setlocal enabledelayedexpansion
>>>>>>> dev

python intro.py

@REM echo ================================
@REM echo 🔄 Устанавливаем pip...
@REM echo ================================
@REM python -m ensurepip --upgrade
@REM python -m pip install --upgrade pip
@REM pip --version
@REM echo ================================
@REM echo 🔄 Проверяем виртуальное окружение...
@REM echo ================================

@REM if exist venv (
@REM     echo ✅ Найдено виртуальное окружение
@REM ) else (
@REM     echo ⚠️ Виртуальное окружение не найдено, создаём...
@REM     python -m venv venv
@REM )

@REM echo ================================
@REM echo 🔄 Активируем виртуальное окружение...
@REM echo ================================
@REM call venv\Scripts\activate
@REM echo ================================
@REM echo 🔄 Устанавливаем зависимости...
@REM echo ================================
@REM pip install --upgrade pip
@REM pip install -r requirements.txt

@REM echo ================================
@REM echo 🚀 Запускаем проект...
@REM echo ================================

<<<<<<< HEAD
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=11911 ^
=======
:: читаем CHROME_PORT из private.env
for /f "tokens=1,2 delims==" %%a in (config.env) do (
    if "%%a"=="CHROME_PORT" set CHROME_PORT=%%b
)

:: запускаем Chrome с портом из env
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=%CHROME_PORT% ^
>>>>>>> dev
  --user-data-dir="C:\chrome-profile"

@REM echo wait...
timeout /t 1 /nobreak >nul

python start.py

echo ================================
echo Завершено!
echo ================================
pause
