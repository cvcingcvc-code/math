@echo off
setlocal
cd /d "%~dp0"
title AI Coding - yu (DeepSeek)

set "CODEX=%LOCALAPPDATA%\OpenAI\Codex\bin\13995fba801849b0\codex.exe"
if not exist "%CODEX%" for /f "delims=" %%i in ('where codex 2^>nul') do set "CODEX=%%i"

echo [start-ai] project: %CD%
echo [start-ai] checking Codex provider config...
where python >nul 2>nul
if errorlevel 1 (
    py -3 "%USERPROFILE%\.codex\repair-deepseek.py" >nul 2>nul
) else (
    python "%USERPROFILE%\.codex\repair-deepseek.py"
)

if not exist "%CODEX%" (
    echo [start-ai] Codex CLI not found. Launching OpenCode Desktop...
    start "" "%LOCALAPPDATA%\Programs\@opencode-aidesktop\OpenCode.exe"
    exit /b 0
)

echo [start-ai] starting Codex CLI (model: deepseek-flash, provider: DeepSeek Official)
echo.
"%CODEX%"
endlocal
