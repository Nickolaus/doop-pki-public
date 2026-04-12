@echo off
setlocal

set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%..
set CERT_PATH=%REPO_ROOT%\certs\doop-root-ca.crt

if not exist "%CERT_PATH%" (
  echo Root certificate not found at "%CERT_PATH%"
  exit /b 1
)

certutil -addstore -f Root "%CERT_PATH%"
if errorlevel 1 exit /b %errorlevel%

echo Installed doop root CA into LocalMachine\Root
