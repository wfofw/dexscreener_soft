@echo off
setlocal EnableExtensions EnableDelayedExpansion

pushd "%~dp0"
chcp 65001 >nul

set "PROJ=%~dp0"
set "VENV=.venv"
set "PY=%VENV%\Scripts\python.exe"
set "PIP=%VENV%\Scripts\pip.exe"

echo [*] CD=%CD%
echo [*] PROJ=%PROJ%

if not exist "%PY%" (
  echo [*] Creating venv...
  py -3.13 -m venv "%VENV%" || goto :fail_venv
)

echo [*] Upgrading pip...
"%PY%" -m pip install --upgrade pip >nul || goto :fail_reqs

echo [*] Files in PROJ:
dir /b "%PROJ%"

set "REQ=%PROJ%requirements.txt"
if exist "%REQ%" (
  echo [*] Installing requirements from "%REQ%"...
  if not exist "%PIP%" (
    echo [!] PIP not found at "%PIP%"
    dir /b "%VENV%\Scripts"
    goto :fail_reqs
  )
  "%PY%" -m pip --version
  "%PY%" -m pip install -r "%REQ%" || goto :fail_reqs
) else (
  echo [!] requirements.txt NOT FOUND at "%REQ%"
  dir /b "%PROJ%"
)

:: ===== CHROME_PORT =====
set "CHROME_PORT="
if exist config.env (
  for /f "usebackq tokens=1,2 delims== eol=#" %%A in ("config.env") do (
    if /I "%%~A"=="CHROME_PORT" set "CHROME_PORT=%%~B"
  )
)
if "%CHROME_PORT%"=="" set "CHROME_PORT=11912"
echo [*] CHROME_PORT=%CHROME_PORT%

:: ===== Chrome DevTools только локально =====
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=%CHROME_PORT% ^
  --remote-debugging-address=127.0.0.1 ^
  --user-data-dir="C:\chrome-profile"

:: ===== Запуск скриптов =====
echo [*] Running: intro.py
"%PY%" intro.py || goto :fail_app

echo [*] Running: start.py
"%PY%" start.py || goto :fail_app

echo.
echo [OK] Done.
goto :end

:fail_venv
echo.
echo [!] venv create failed
where py
py -0p
python -V 2>&1
goto :end

:fail_reqs
echo.
echo [!] pip install failed
type "%REQ%" 2>nul
goto :end

:fail_app
echo.
echo [!] app failed (see error above)
goto :end

:end
popd
endlocal
pause