@echo off

cd C:\Users\monolith\wkspaces\spicy

echo update server
pause

git pull

echo startup server
pause

C:\Users\monolith\wkspaces\spicy\.venv\Scripts\python.exe C:\Users\monolith\wkspaces\spicy\main.py

echo shutdown server
pause
