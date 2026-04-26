@echo off
cd /d C:\Users\Andrea\OneDrive\Desktop\mes\backend
call venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
