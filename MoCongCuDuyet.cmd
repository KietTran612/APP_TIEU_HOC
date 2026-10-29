@echo off
rem Bấm đúp để mở công cụ duyệt âm thanh và tranh. Đóng cửa sổ này để tắt công cụ.
chcp 65001 >nul
set PYTHONUTF8=1
title Công cụ duyệt âm thanh và tranh - Tập đọc
cd /d "%~dp0tools"

set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && set "PY=py -3"
if not defined PY goto khong_co_python

%PY% -m tapdoc mo
if errorlevel 1 pause
exit /b

:khong_co_python
echo Không tìm thấy Python 3 trên máy. Cài Python 3.14 rồi bấm đúp lại file này.
pause
