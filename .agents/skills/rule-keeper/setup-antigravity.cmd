@echo off
rem Setup rule-keeper cho Antigravity. Bam dup file nay, hoac chay tu terminal.
setlocal
where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo [rule-keeper] Chua co Node.js tren may nay.
  echo Cai ban LTS tai https://nodejs.org roi chay lai file nay.
  echo.
  pause
  exit /b 1
)
node "%~dp0setup.mjs" antigravity %*
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%
