@echo off
REM ============================================================================
REM Screaming Frog Crawl Automation Script (Windows)
REM ============================================================================
REM
REM Usage: run_screaming_frog_crawl.bat [target_url]
REM
REM This script runs the Screaming Frog automation with proper logging
REM and error handling. Suitable for Windows Task Scheduler.
REM
REM Task Scheduler Setup:
REM 1. Open Task Scheduler
REM 2. Create Basic Task
REM 3. Trigger: Daily at 2:00 AM
REM 4. Action: Start a program
REM 5. Program: C:\path\to\run_screaming_frog_crawl.bat
REM 6. Arguments: https://bs-company.ch
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
set "PYTHON_SCRIPT=%PROJECT_DIR%\apps\api\crawl_and_ingest.py"
set "ENV_FILE=%PROJECT_DIR%\.env.screamingfrog.local"
set "LOG_DIR=%PROJECT_DIR%\logs"
set "VENV_DIR=%PROJECT_DIR%\venv"

REM Create logs directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Generate timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%"
set "LOG_FILE=%LOG_DIR%\crawl_%datetime:~0,8%_%datetime:~8,6%.log"

REM Logging function
call :log "============================================================"
call :log "Screaming Frog Crawl Started"
call :log "============================================================"

REM Activate virtual environment if it exists
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call :log "Activating virtual environment: %VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    call :log "Warning: No virtual environment found at %VENV_DIR%"
)

REM Load environment variables
if exist "%ENV_FILE%" (
    call :log "Loading environment from: %ENV_FILE%"
    for /f "usebackq tokens=*" %%a in ("%ENV_FILE%") do (
        set "%%a"
    )
) else (
    call :log "Warning: Environment file not found: %ENV_FILE%"
)

REM Resolve TARGET_URL with precedence: arg > env > data\target_url.txt
set "TARGET_SOURCE=env"
if not "%~1"=="" (
    set "TARGET_URL=%~1"
    set "TARGET_SOURCE=cli"
) else if "%TARGET_URL%"=="" (
    set "TARGET_FILE=%PROJECT_DIR%\data\target_url.txt"
    if exist "%TARGET_FILE%" (
        for /f "usebackq delims=" %%u in ("%TARGET_FILE%") do (
            if not "%%u"=="" (
                set "TARGET_URL=%%u"
                goto :afterFileRead
            )
        )
        :afterFileRead
        if not "%TARGET_URL%"=="" set "TARGET_SOURCE=file:%TARGET_FILE%"
    )
)
call :log "Target URL: %TARGET_URL% (source: %TARGET_SOURCE%)"

REM Check Python script exists
if not exist "%PYTHON_SCRIPT%" (
    call :log "ERROR: Python script not found: %PYTHON_SCRIPT%"
    exit /b 1
)

REM Run the crawl
call :log "Starting crawl..."
if not "%TARGET_URL%"=="" (
    call :log "Command: python %PYTHON_SCRIPT% --target-url %TARGET_URL%"
) else (
    call :log "Command: python %PYTHON_SCRIPT%"
)
call :log "------------------------------------------------------------"

if not "%TARGET_URL%"=="" (
    python "%PYTHON_SCRIPT%" --target-url "%TARGET_URL%" >> "%LOG_FILE%" 2>&1
) else (
    python "%PYTHON_SCRIPT%" >> "%LOG_FILE%" 2>&1
)
set CRAWL_EXIT_CODE=%ERRORLEVEL%

call :log "------------------------------------------------------------"

if %CRAWL_EXIT_CODE% equ 0 (
    call :log "✓ Crawl completed successfully (exit code: %CRAWL_EXIT_CODE%)"
    
    REM Optional: Send success notification
    REM curl -X POST https://hooks.slack.com/... -d "{\"text\":\"Crawl succeeded\"}"
    
    exit /b 0
) else (
    call :log "✗ Crawl failed (exit code: %CRAWL_EXIT_CODE%)"
    
    REM Optional: Send error notification
    REM curl -X POST https://hooks.slack.com/... -d "{\"text\":\"Crawl failed!\"}"
    
    exit /b %CRAWL_EXIT_CODE%
)

REM Logging subroutine
:log
echo [%TIMESTAMP%] %~1
echo [%TIMESTAMP%] %~1 >> "%LOG_FILE%"
goto :eof
