@echo off
echo ========================================================
echo   Deploying PresensiDosenPro to Vercel...
echo ========================================================
cd /d "%~dp0"
npx.cmd vercel
pause
