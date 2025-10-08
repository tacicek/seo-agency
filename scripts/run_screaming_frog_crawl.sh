#!/bin/bash
# ============================================================================
# Screaming Frog Crawl Automation Script (macOS/Linux)
# ============================================================================
#
# Usage: ./run_screaming_frog_crawl.sh [target_url]
#
# This script runs the Screaming Frog automation with proper logging
# and error handling. Suitable for cron jobs.
#
# Cron example (daily at 2 AM):
# 0 2 * * * /path/to/run_screaming_frog_crawl.sh https://bs-company.ch
# ============================================================================

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${PROJECT_DIR}/venv"
LOG_DIR="${PROJECT_DIR}/logs"
PYTHON_SCRIPT="${PROJECT_DIR}/apps/api/crawl_and_ingest.py"
ENV_FILE="${PROJECT_DIR}/.env.screamingfrog.local"

# Create logs directory
mkdir -p "$LOG_DIR"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="${LOG_DIR}/crawl_$(date '+%Y%m%d_%H%M%S').log"

# Logging function
log() {
    echo "[${TIMESTAMP}] $*" | tee -a "$LOG_FILE"
}

log "============================================================"
log "Screaming Frog Crawl Started"
log "============================================================"

# Check if virtual environment exists
if [ -d "$VENV_DIR" ]; then
    log "Activating virtual environment: $VENV_DIR"
    source "$VENV_DIR/bin/activate"
else
    log "Warning: No virtual environment found at $VENV_DIR"
fi

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    log "Loading environment from: $ENV_FILE"
    set -a  # Export all variables
    source "$ENV_FILE"
    set +a
else
    log "Warning: Environment file not found: $ENV_FILE"
fi

# Resolve TARGET_URL with precedence: arg > env > data/target_url.txt
TARGET_SOURCE="env"
if [ $# -ge 1 ] && [ -n "${1:-}" ]; then
    export TARGET_URL="$1"
    TARGET_SOURCE="cli"
elif [ -z "${TARGET_URL:-}" ]; then
    TARGET_FILE="${PROJECT_DIR}/data/target_url.txt"
    if [ -f "$TARGET_FILE" ]; then
        export TARGET_URL="$(head -n 1 "$TARGET_FILE" | tr -d '\r' | xargs)"
        if [ -n "$TARGET_URL" ]; then
            TARGET_SOURCE="file:$TARGET_FILE"
        fi
    fi
fi

log "Target URL: ${TARGET_URL:-not set} (source: $TARGET_SOURCE)"

# Check Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log "ERROR: Python script not found: $PYTHON_SCRIPT"
    exit 1
fi

# Run the crawl
log "Starting crawl..."
if [ -n "${TARGET_URL:-}" ]; then
    log "Command: python $PYTHON_SCRIPT --target-url $TARGET_URL"
else
    log "Command: python $PYTHON_SCRIPT"
fi
log "------------------------------------------------------------"

if [ -n "${TARGET_URL:-}" ]; then
    if python "$PYTHON_SCRIPT" --target-url "$TARGET_URL" 2>&1 | tee -a "$LOG_FILE"; then
        EXIT_CODE=$?
        log "------------------------------------------------------------"
        log "✓ Crawl completed successfully (exit code: $EXIT_CODE)"
        
        # Optional: Send success notification
        # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl succeeded"}'
        
        exit 0
    else
        EXIT_CODE=$?
        log "------------------------------------------------------------"
        log "✗ Crawl failed (exit code: $EXIT_CODE)"
        
        # Optional: Send error notification
        # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl failed!"}'
        
        exit $EXIT_CODE
    fi
else
    if python "$PYTHON_SCRIPT" 2>&1 | tee -a "$LOG_FILE"; then
        EXIT_CODE=$?
        log "------------------------------------------------------------"
        log "✓ Crawl completed successfully (exit code: $EXIT_CODE)"
        
        # Optional: Send success notification
        # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl succeeded"}'
        
        exit 0
    else
        EXIT_CODE=$?
        log "------------------------------------------------------------"
        log "✗ Crawl failed (exit code: $EXIT_CODE)"
        
        # Optional: Send error notification
        # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl failed!"}'
        
        exit $EXIT_CODE
    fi
fi
    EXIT_CODE=$?
    log "------------------------------------------------------------"
    log "✓ Crawl completed successfully (exit code: $EXIT_CODE)"
    
    # Optional: Send success notification
    # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl succeeded"}'
    
    exit 0
else
    EXIT_CODE=$?
    log "------------------------------------------------------------"
    log "✗ Crawl failed (exit code: $EXIT_CODE)"
    
    # Optional: Send error notification
    # curl -X POST https://hooks.slack.com/... -d '{"text":"Crawl failed!"}'
    
    exit $EXIT_CODE
fi
