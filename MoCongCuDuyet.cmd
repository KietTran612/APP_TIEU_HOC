@echo off
rem Bấm đúp để mở công cụ duyệt âm thanh và tranh. Đóng cửa sổ này để tắt công cụ.
chcp 65001 >nul
set PYTHONUTF8=1
title Công cụ duyệt âm thanh và tranh - Tập đọc
cd /d "%~dp0tools"

set "PY="
rem Chạy thử chứ không chỉ "where": "python" giả của Microsoft Store có trong PATH nhưng không chạy được.
rem "call" để python dạng .bat/.cmd (vd. pyenv-win) không làm dừng file này.
call python -c "import sys" >nul 2>nul && set "PY=python"
if not defined PY call py -3 -c "import sys" >nul 2>nul && set "PY=py -3"
if not defined PY goto khong_co_python

call %PY% -m tapdoc mo
if errorlevel 1 pause
exit /b

:khong_co_python
echo Không tìm thấy Python 3 trên máy. Cài Python 3.14 rồi bấm đúp lại file này.
pause
