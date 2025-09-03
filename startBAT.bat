@echo off
chcp 65001 >nul

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

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=11911 ^
  --user-data-dir="C:\chrome-profile"

@REM echo wait...
timeout /t 1 /nobreak >nul

python start.py

echo ================================
echo Завершено!
echo ================================
pause
