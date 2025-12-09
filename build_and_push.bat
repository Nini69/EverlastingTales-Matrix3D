@echo off
cd /d "%~dp0"
set IMAGE_NAME=ghcr.io/nini69/matrix3d:latest

echo [BUILD] Building Docker image %IMAGE_NAME%...
docker build -t %IMAGE_NAME% .

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker build failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [PUSH] Pushing image to GHCR...
echo (Make sure you are logged in: docker login ghcr.io -u YOUR_USERNAME -p YOUR_TOKEN)
docker push %IMAGE_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker push failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] Image built and pushed successfully!
pause
