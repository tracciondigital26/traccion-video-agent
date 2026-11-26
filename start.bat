@echo off
title Agente Grip Video - Traccion Digital
echo ============================================================
echo   Iniciando Agente Grip Video de Traccion Digital
echo ============================================================
set "PATH=%USERPROFILE%\mingit\cmd;%PATH%"

echo 1. Iniciando servidor local en http://localhost:5000...
start "Traccion Digital Server" /min python app.py

echo 2. Conectando al Tunel Oficial de Cloudflare...
timeout /t 3 /nobreak >nul
start "Cloudflare Tunnel" cloudflared.exe tunnel run --token eyJhIjoiYjFiZDNjZWJlMjk4Njc2MzQxNGY4NjhjMjhhZmJiMWYiLCJ0IjoiNTliOWFkZmMtYTZkMy00ZWJhLWJjNjgtNjk1ZjgwZDMwMGY1IiwicyI6Ik5EVTJaak5oTVRJdFlXUmxOUzAwWWpRNUxUZzVPVGd0Tm1Sa05qVTROVEF5TnpGaiJ9

echo ============================================================
echo   Listo! Servidor y Tunel Oficial de Cloudflare Conectados.
echo ============================================================
pause
