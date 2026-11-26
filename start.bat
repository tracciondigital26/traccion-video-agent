@echo off
title Agente Grip Video - Traccion Digital
echo ============================================================
echo   Iniciando Agente Grip Video de Traccion Digital
echo ============================================================
set "PATH=%USERPROFILE%\mingit\cmd;%PATH%"

echo 1. Iniciando servidor local en http://localhost:5000...
start "Traccion Digital Server" /min python app.py

echo 2. Iniciando tunel seguro de Cloudflare...
timeout /t 3 /nobreak >nul
start "Cloudflare Tunnel" cloudflared tunnel --url http://localhost:5000

echo ============================================================
echo   Listo! Servidor y Tunel Cloudflare activos.
echo ============================================================
pause
