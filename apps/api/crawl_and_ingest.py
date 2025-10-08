#!/usr/bin/env python3
"""
Screaming Frog SEO Spider Automation System
============================================

Production-ready Python system that integrates Screaming Frog CLI
to crawl websites, normalize data with pandas, and upload to Supabase.

Author: SEO Automation Engineer
Date: 2025-10-07
Version: 1.0.0

Features:
- Headless Screaming Frog CLI crawling
- CSV data export and normalization
- Supabase integration for data storage
- Timestamped report directories
- Error handling and logging
- Cross-platform support (macOS/Windows)
- Cron/n8n automation ready

Usage:
    python crawl_and_ingest.py

Environment Variables:
    TARGET_URL          - Website to crawl (default: https://bs-company.ch)
    SF_BIN             - Path to Screaming Frog CLI binary
    REPORTS_DIR        - Base directory for reports (default: ./reports)
    SUPABASE_URL       - Supabase project URL
    SUPABASE_KEY       - Supabase service role key
    SUPABASE_TABLE     - Table name (default: seo_crawl_pages)
    MAX_CRAWL_DEPTH    - Maximum crawl depth (default: 3)
    MAX_PAGES          - Maximum pages to crawl (default: 1000)
"""

import os
import sys
import json
import logging
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration management from environment variables"""
    
    # Target website
    TARGET_URL = os.getenv('TARGET_URL', 'https://bs-company.ch')
    
    # Screaming Frog binary paths (auto-detect platform)
    if sys.platform == 'darwin':  # macOS
        SF_BIN_DEFAULT = '/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli'
    elif sys.platform == 'win32':  # Windows
        SF_BIN_DEFAULT = r'C:\Program Files\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe'
    else:  # Linux
        SF_BIN_DEFAULT = '/usr/local/bin/ScreamingFrogSEOSpiderCli'
    
    SF_BIN = os.getenv('SF_BIN', SF_BIN_DEFAULT)
    
    # Report directories
    REPORTS_DIR = Path(os.getenv('REPORTS_DIR', './reports'))
    
    # Crawl settings
    MAX_CRAWL_DEPTH = int(os.getenv('MAX_CRAWL_DEPTH', '3'))
    MAX_PAGES = int(os.getenv('MAX_PAGES', '1000'))
    
    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    SUPABASE_TABLE = os.getenv('SUPABASE_TABLE', 'seo_crawl_pages')
    
    # Batch upload size
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '500'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_dir: Optional[Path] = None) -> logging.Logger:
    """
    Configure logging with console and optional file output
    
    Args:
        log_dir: Optional directory for log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('screaming_frog_automation')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_dir provided)
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / 'crawl.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Initialize logger
logger = setup_logging()


# ============================================================================
# SCREAMING FROG CLI INTEGRATION
# ============================================================================

def check_screaming_frog_installed() -> bool:
    """
    Check if Screaming Frog CLI is installed and accessible
    
    Returns:
        True if binary exists, False otherwise
    """
    sf_path = Path(Config.SF_BIN)
    
    if not sf_path.exists():
        logger.error(f"Screaming Frog CLI not found at: {Config.SF_BIN}")
        logger.error("Please install Screaming Frog SEO Spider or set SF_BIN environment variable")
        return False
    
    logger.info(f"✓ Screaming Frog CLI found at: {Config.SF_BIN}")
    return True


def create_output_directory() -> Path:
    """
    Create timestamped output directory for reports
    
    Returns:
        Path to created directory
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Config.REPORTS_DIR / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"✓ Created output directory: {output_dir}")
    return output_dir


def run_screaming_frog(url: str, output_dir: Path) -> Tuple[bool, str]:
    """
    Execute Screaming Frog CLI to crawl a website
    
    Args:
        url: Target URL to crawl
        output_dir: Directory to save export files
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    logger.info(f"Starting Screaming Frog crawl for: {url}")
    logger.info(f"Max depth: {Config.MAX_CRAWL_DEPTH}, Max pages: {Config.MAX_PAGES}")
    
    try:
        # Build command
        cmd = [
            Config.SF_BIN,
            '--crawl', url,
            '--headless',
            '--output-folder', str(output_dir),
            '--export-tabs', 'Internal:All,PageTitles:All,MetaDescription:All,H1:All,H2:All,Images:All',
            '--max-crawl-depth', str(Config.MAX_CRAWL_DEPTH),
            '--max-crawl-urls', str(Config.MAX_PAGES),
            '--save-crawl',
            '--overwrite'
        ]
        
        logger.debug(f"Command: {' '.join(cmd)}")
        
        # Execute crawl
        start_time = time.time()
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor progress
        stdout_lines = []
        stderr_lines = []
        
        for line in process.stdout:
            line = line.strip()
            if line:
                stdout_lines.append(line)
                if 'crawling' in line.lower() or 'exported' in line.lower():
                    logger.info(f"SF: {line}")
        
        for line in process.stderr:
            line = line.strip()
            if line:
                stderr_lines.append(line)
                logger.warning(f"SF Warning: {line}")
        
        # Wait for completion
        return_code = process.wait()
        elapsed = time.time() - start_time
        
        if return_code == 0:
            logger.info(f"✓ Crawl completed successfully in {elapsed:.1f}s")
            return True, f"Crawl completed in {elapsed:.1f}s"
        else:
            error_msg = '\n'.join(stderr_lines[-10:])  # Last 10 error lines
            logger.error(f"✗ Crawl failed with return code {return_code}")
            logger.error(f"Error: {error_msg}")
            return False, f"Crawl failed: {error_msg}"
            
    except FileNotFoundError:
        error_msg = f"Screaming Frog CLI not found at: {Config.SF_BIN}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error during crawl: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg


# ============================================================================
# DATA EXPORT & NORMALIZATION
# ============================================================================

def find_export_files(output_dir: Path) -> Dict[str, Optional[Path]]:
    """
    Locate exported CSV files from Screaming Frog
    
    Args:
        output_dir: Directory containing exports
        
    Returns:
        Dictionary mapping export type to file path
    """
    exports = {
        'internal': None,
        'page_titles': None,
        'meta_description': None,
        'h1': None,
        'h2': None,
        'images': None
    }
    
    # Common file naming patterns
    patterns = {
        'internal': ['internal_all.csv', 'internal.csv'],
        'page_titles': ['page_titles_all.csv', 'page_titles.csv'],
        'meta_description': ['meta_description_all.csv', 'meta_description.csv'],
        'h1': ['h1_all.csv', 'h1.csv', 'h1_1.csv'],
        'h2': ['h2_all.csv', 'h2.csv', 'h2_1.csv'],
        'images': ['images_all.csv', 'images.csv']
    }
    
    for export_type, file_patterns in patterns.items():
        for pattern in file_patterns:
            file_path = output_dir / pattern
            if file_path.exists():
                exports[export_type] = file_path
                logger.debug(f"Found {export_type}: {file_path.name}")
                break
    
    # Log found files
    found = [k for k, v in exports.items() if v is not None]
    logger.info(f"✓ Found {len(found)} export files: {', '.join(found)}")
    
    return exports


def load_exports(output_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Load all exported CSV files into pandas DataFrames
    
    Args:
        output_dir: Directory containing CSV exports
        
    Returns:
        Dictionary mapping export type to DataFrame
    """
    logger.info("Loading CSV exports...")
    
    export_files = find_export_files(output_dir)
    dataframes = {}
    
    for export_type, file_path in export_files.items():
        if file_path is None:
            logger.warning(f"⚠ {export_type} export not found")
            continue
            
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            dataframes[export_type] = df
            logger.info(f"✓ Loaded {export_type}: {len(df)} rows, {len(df.columns)} columns")
            
        except Exception as e:
            logger.error(f"✗ Failed to load {export_type}: {str(e)}")
    
    return dataframes


def normalize_pages(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Normalize and merge crawl data into a single clean dataset
    
    Args:
        dataframes: Dictionary of exported DataFrames
        
    Returns:
        Normalized pandas DataFrame
    """
    logger.info("Normalizing crawl data...")
    
    # Start with internal pages
    if 'internal' not in dataframes:
        raise ValueError("Internal pages export is required")
    
    df = dataframes['internal'].copy()
    
    # Standardize column names (Screaming Frog uses various formats)
    column_mapping = {
        'Address': 'url',
        'Status Code': 'status_code',
        'Status': 'status_code',
        'Content': 'content_type',
        'Content Type': 'content_type',
        'Word Count': 'word_count',
        'Indexability': 'indexability',
        'Indexability Status': 'indexability',
    }
    
    df.rename(columns=column_mapping, inplace=True)
    
    # Ensure required columns exist
    required_columns = ['url', 'status_code']
    for col in required_columns:
        if col not in df.columns:
            logger.warning(f"⚠ Missing required column: {col}")
    
    # Merge page titles
    if 'page_titles' in dataframes:
        titles_df = dataframes['page_titles'].copy()
        if 'Address' in titles_df.columns and 'Title 1' in titles_df.columns:
            titles_df.rename(columns={'Address': 'url', 'Title 1': 'title'}, inplace=True)
            df = df.merge(titles_df[['url', 'title']], on='url', how='left')
            logger.debug("✓ Merged page titles")
    
    # Merge meta descriptions
    if 'meta_description' in dataframes:
        desc_df = dataframes['meta_description'].copy()
        if 'Address' in desc_df.columns and 'Meta Description 1' in desc_df.columns:
            desc_df.rename(columns={'Address': 'url', 'Meta Description 1': 'description'}, inplace=True)
            df = df.merge(desc_df[['url', 'description']], on='url', how='left')
            logger.debug("✓ Merged meta descriptions")
    
    # Merge H1 tags
    if 'h1' in dataframes:
        h1_df = dataframes['h1'].copy()
        if 'Address' in h1_df.columns and 'H1-1' in h1_df.columns:
            h1_df.rename(columns={'Address': 'url', 'H1-1': 'h1'}, inplace=True)
            df = df.merge(h1_df[['url', 'h1']], on='url', how='left')
            logger.debug("✓ Merged H1 tags")
    
    # Select and order final columns
    final_columns = [
        'url', 'status_code', 'title', 'description', 'h1',
        'word_count', 'content_type', 'indexability'
    ]
    
    # Keep only columns that exist
    available_columns = [col for col in final_columns if col in df.columns]
    df_normalized = df[available_columns].copy()
    
    # Add metadata
    df_normalized['crawl_timestamp'] = datetime.now().isoformat()
    df_normalized['source_domain'] = Config.TARGET_URL
    
    # Clean data
    df_normalized.fillna('', inplace=True)
    
    # Convert status codes to integers
    if 'status_code' in df_normalized.columns:
        df_normalized['status_code'] = pd.to_numeric(
            df_normalized['status_code'], 
            errors='coerce'
        ).fillna(0).astype(int)
    
    logger.info(f"✓ Normalized {len(df_normalized)} pages with {len(df_normalized.columns)} columns")
    
    return df_normalized


def save_normalized_data(df: pd.DataFrame, output_dir: Path) -> Path:
    """
    Save normalized data to CSV
    
    Args:
        df: Normalized DataFrame
        output_dir: Output directory
        
    Returns:
        Path to saved file
    """
    output_file = output_dir / 'normalized_pages.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    logger.info(f"✓ Saved normalized data: {output_file}")
    
    return output_file


def generate_summary(df: pd.DataFrame, output_dir: Path) -> Dict:
    """
    Generate crawl summary statistics
    
    Args:
        df: Normalized DataFrame
        output_dir: Output directory for JSON file
        
    Returns:
        Summary dictionary
    """
    summary = {
        'crawl_timestamp': datetime.now().isoformat(),
        'target_url': Config.TARGET_URL,
        'total_pages': len(df),
        'pages_by_status': {},
        'indexable_pages': 0,
        'pages_with_titles': 0,
        'pages_with_descriptions': 0,
        'avg_word_count': 0
    }
    
    # Status code distribution
    if 'status_code' in df.columns:
        status_counts = df['status_code'].value_counts().to_dict()
        summary['pages_by_status'] = {int(k): int(v) for k, v in status_counts.items()}
        summary['pages_200'] = int(status_counts.get(200, 0))
    
    # Indexability
    if 'indexability' in df.columns:
        summary['indexable_pages'] = int((df['indexability'] == 'Indexable').sum())
    
    # Content completeness
    if 'title' in df.columns:
        summary['pages_with_titles'] = int((df['title'] != '').sum())
    
    if 'description' in df.columns:
        summary['pages_with_descriptions'] = int((df['description'] != '').sum())
    
    # Word count
    if 'word_count' in df.columns:
        summary['avg_word_count'] = float(df['word_count'].mean())
    
    # Save to JSON
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"✓ Generated summary: {summary_file}")
    logger.info(f"  Total pages: {summary['total_pages']}")
    logger.info(f"  200 Status: {summary.get('pages_200', 0)}")
    logger.info(f"  Indexable: {summary['indexable_pages']}")
    
    return summary


# ============================================================================
# SUPABASE INTEGRATION
# ============================================================================

def get_supabase_session() -> requests.Session:
    """
    Create requests session with retry logic for Supabase API
    
    Returns:
        Configured requests Session
    """
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers
    session.headers.update({
        'apikey': Config.SUPABASE_KEY,
        'Authorization': f'Bearer {Config.SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    })
    
    return session


def upload_to_supabase(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Upload normalized data to Supabase table
    
    Args:
        df: Normalized DataFrame to upload
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
        logger.warning("⚠ Supabase credentials not configured - skipping upload")
        return False, "Supabase not configured"
    
    logger.info(f"Uploading {len(df)} rows to Supabase table: {Config.SUPABASE_TABLE}")
    
    try:
        session = get_supabase_session()
        endpoint = f"{Config.SUPABASE_URL}/rest/v1/{Config.SUPABASE_TABLE}"
        
        # Convert DataFrame to list of dicts
        records = df.to_dict('records')
        
        # Upload in batches
        total_batches = (len(records) + Config.BATCH_SIZE - 1) // Config.BATCH_SIZE
        uploaded = 0
        
        for batch_num in range(total_batches):
            start_idx = batch_num * Config.BATCH_SIZE
            end_idx = min(start_idx + Config.BATCH_SIZE, len(records))
            batch = records[start_idx:end_idx]
            
            logger.info(f"Uploading batch {batch_num + 1}/{total_batches} ({len(batch)} rows)...")
            
            response = session.post(endpoint, json=batch, timeout=30)
            
            if response.status_code in [200, 201]:
                uploaded += len(batch)
                logger.debug(f"✓ Batch {batch_num + 1} uploaded successfully")
            else:
                error_msg = f"Failed to upload batch {batch_num + 1}: {response.status_code} {response.text}"
                logger.error(error_msg)
                return False, error_msg
        
        logger.info(f"✓ Successfully uploaded {uploaded} rows to Supabase")
        return True, f"Uploaded {uploaded} rows"
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error during upload: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error during upload: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def _resolve_target_url(cli_target: Optional[str] = None) -> Tuple[str, str]:
    """
    Resolve TARGET_URL with clear precedence:
    1) CLI argument --target-url
    2) Environment variable TARGET_URL
    3) data/target_url.txt (first line)
    4) Default in code (https://bs-company.ch)

    Returns:
        (resolved_url, source)
    """
    # 1) CLI argument
    if cli_target and cli_target.strip():
        return cli_target.strip(), "cli"

    # 2) Environment variable
    env_val = os.getenv('TARGET_URL')
    if env_val and env_val.strip():
        return env_val.strip(), "env"

    # 3) File fallback
    try:
        # Host/dev environment: repo_root/data/target_url.txt
        try:
            project_root = Path(__file__).resolve().parents[2]
            target_file = project_root / 'data' / 'target_url.txt'
            if target_file.exists():
                content = target_file.read_text(encoding='utf-8').strip()
                if content:
                    return content, f"file:{target_file}"
        except IndexError:
            # In containers, parents[2] may not exist; ignore and try /data
            pass

        # Docker container: /data/target_url.txt (volume mounted)
        container_file = Path('/data/target_url.txt')
        if container_file.exists():
            content = container_file.read_text(encoding='utf-8').strip()
            if content:
                return content, f"file:{container_file}"
    except Exception:
        # Non-fatal: ignore file read issues
        pass

    # 4) Default
    return 'https://bs-company.ch', 'default'

def main():
    """
    Main execution flow
    """
    # Parse CLI arguments early to resolve TARGET_URL before logging
    parser = argparse.ArgumentParser(description='Screaming Frog SEO Spider Automation')
    parser.add_argument('-t', '--target-url', help='Target URL to crawl (overrides env/file)')
    args = parser.parse_args()

    resolved_url, source = _resolve_target_url(args.target_url)
    # Propagate to env and config for downstream functions
    os.environ['TARGET_URL'] = resolved_url
    Config.TARGET_URL = resolved_url

    logger.info("=" * 70)
    logger.info("Screaming Frog SEO Spider Automation")
    logger.info("=" * 70)
    logger.info(f"Target URL: {Config.TARGET_URL}  (source: {source})")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
    
    # Step 1: Check prerequisites
    logger.info("\n[1/6] Checking prerequisites...")
    if not check_screaming_frog_installed():
        logger.error("✗ Prerequisites check failed")
        return 1
    
    # Step 2: Create output directory
    logger.info("\n[2/6] Creating output directory...")
    output_dir = create_output_directory()
    
    # Setup file logging
    global logger
    logger = setup_logging(output_dir)
    
    # Step 3: Run Screaming Frog crawl
    logger.info("\n[3/6] Running Screaming Frog crawl...")
    success, message = run_screaming_frog(Config.TARGET_URL, output_dir)
    
    if not success:
        logger.error(f"✗ Crawl failed: {message}")
        return 1
    
    # Step 4: Load and normalize data
    logger.info("\n[4/6] Loading and normalizing crawl data...")
    try:
        dataframes = load_exports(output_dir)
        
        if not dataframes:
            logger.error("✗ No export files found")
            return 1
        
        df_normalized = normalize_pages(dataframes)
        
        # Save normalized data
        save_normalized_data(df_normalized, output_dir)
        
        # Generate summary
        summary = generate_summary(df_normalized, output_dir)
        
    except Exception as e:
        logger.error(f"✗ Data processing failed: {str(e)}", exc_info=True)
        return 1
    
    # Step 5: Upload to Supabase (optional)
    logger.info("\n[5/6] Uploading to Supabase...")
    if Config.SUPABASE_URL and Config.SUPABASE_KEY:
        success, message = upload_to_supabase(df_normalized)
        if success:
            logger.info(f"✓ {message}")
        else:
            logger.warning(f"⚠ Upload failed: {message}")
    else:
        logger.info("⊘ Supabase upload skipped (credentials not configured)")
    
    # Step 6: Final summary
    logger.info("\n[6/6] Crawl completed successfully!")
    logger.info("=" * 70)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Total pages crawled: {summary['total_pages']}")
    logger.info(f"Pages with 200 status: {summary.get('pages_200', 0)}")
    logger.info(f"Indexable pages: {summary['indexable_pages']}")
    logger.info(f"Normalized data: {output_dir / 'normalized_pages.csv'}")
    logger.info(f"Summary: {output_dir / 'summary.json'}")
    logger.info("=" * 70)
    
    return 0


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.warning("\n⚠ Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"✗ Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
