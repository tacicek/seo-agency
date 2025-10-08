-- ============================================================================
-- Screaming Frog Crawl Data Table
-- ============================================================================
-- 
-- Stores normalized crawl data from Screaming Frog SEO Spider
-- Supports multiple domains and historical tracking
--
-- Created: 2025-10-07
-- Version: 1.0.0
-- ============================================================================

-- Drop existing table (optional - uncomment if recreating)
-- DROP TABLE IF EXISTS seo_crawl_pages CASCADE;

-- Create main crawl data table
CREATE TABLE IF NOT EXISTS seo_crawl_pages (
  -- Primary key
  id BIGSERIAL PRIMARY KEY,
  
  -- Page identification
  url TEXT NOT NULL,
  source_domain TEXT NOT NULL,
  
  -- HTTP response
  status_code INTEGER,
  content_type TEXT,
  
  -- SEO elements
  title TEXT,
  description TEXT,
  h1 TEXT,
  
  -- Content metrics
  word_count INTEGER DEFAULT 0,
  indexability TEXT,
  
  -- Timestamps
  crawl_timestamp TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Optional metadata
  meta JSONB DEFAULT '{}'::JSONB
);

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- URL lookup (exact match)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_url 
ON seo_crawl_pages(url);

-- Domain filtering
CREATE INDEX IF NOT EXISTS idx_seo_crawl_domain 
ON seo_crawl_pages(source_domain);

-- Status code filtering (find errors)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_status 
ON seo_crawl_pages(status_code);

-- Timestamp sorting (historical data)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_timestamp 
ON seo_crawl_pages(crawl_timestamp DESC);

-- Combined index for domain + timestamp queries
CREATE INDEX IF NOT EXISTS idx_seo_crawl_domain_timestamp 
ON seo_crawl_pages(source_domain, crawl_timestamp DESC);

-- Text search on titles (optional)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_title_gin 
ON seo_crawl_pages USING GIN(to_tsvector('english', COALESCE(title, '')));

-- Text search on descriptions (optional)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_desc_gin 
ON seo_crawl_pages USING GIN(to_tsvector('english', COALESCE(description, '')));

-- JSONB metadata index (optional)
CREATE INDEX IF NOT EXISTS idx_seo_crawl_meta 
ON seo_crawl_pages USING GIN(meta);

-- ============================================================================
-- ROW LEVEL SECURITY (Optional)
-- ============================================================================

-- Enable RLS
ALTER TABLE seo_crawl_pages ENABLE ROW LEVEL SECURITY;

-- Policy: Allow service role full access
CREATE POLICY "Service role has full access" 
ON seo_crawl_pages
FOR ALL 
TO service_role
USING (true)
WITH CHECK (true);

-- Policy: Allow authenticated users to read
CREATE POLICY "Authenticated users can read" 
ON seo_crawl_pages
FOR SELECT 
TO authenticated
USING (true);

-- Policy: Allow authenticated users to insert (optional)
CREATE POLICY "Authenticated users can insert" 
ON seo_crawl_pages
FOR INSERT 
TO authenticated
WITH CHECK (true);

-- ============================================================================
-- VIEWS for Common Queries
-- ============================================================================

-- Latest crawl per domain
CREATE OR REPLACE VIEW latest_crawls AS
SELECT DISTINCT ON (source_domain)
  source_domain,
  crawl_timestamp,
  COUNT(*) OVER (PARTITION BY source_domain, crawl_timestamp) as total_pages
FROM seo_crawl_pages
ORDER BY source_domain, crawl_timestamp DESC;

-- Pages with issues
CREATE OR REPLACE VIEW pages_with_issues AS
SELECT 
  url,
  source_domain,
  status_code,
  title,
  description,
  word_count,
  crawl_timestamp,
  CASE 
    WHEN status_code != 200 THEN 'HTTP Error'
    WHEN title IS NULL OR title = '' THEN 'Missing Title'
    WHEN description IS NULL OR description = '' THEN 'Missing Description'
    WHEN word_count < 300 THEN 'Thin Content'
    ELSE 'Unknown'
  END as issue_type
FROM seo_crawl_pages
WHERE status_code != 200
   OR title IS NULL OR title = ''
   OR description IS NULL OR description = ''
   OR word_count < 300;

-- Status code summary
CREATE OR REPLACE VIEW status_summary AS
SELECT 
  source_domain,
  crawl_timestamp,
  status_code,
  COUNT(*) as count
FROM seo_crawl_pages
GROUP BY source_domain, crawl_timestamp, status_code
ORDER BY source_domain, crawl_timestamp DESC, status_code;

-- SEO health score
CREATE OR REPLACE VIEW seo_health_scores AS
SELECT 
  source_domain,
  crawl_timestamp,
  COUNT(*) as total_pages,
  SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as pages_200,
  SUM(CASE WHEN title IS NOT NULL AND title != '' THEN 1 ELSE 0 END) as pages_with_title,
  SUM(CASE WHEN description IS NOT NULL AND description != '' THEN 1 ELSE 0 END) as pages_with_description,
  SUM(CASE WHEN word_count >= 300 THEN 1 ELSE 0 END) as pages_good_content,
  ROUND(
    (SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END)::DECIMAL / COUNT(*)) * 100, 
    2
  ) as health_score_pct
FROM seo_crawl_pages
GROUP BY source_domain, crawl_timestamp
ORDER BY crawl_timestamp DESC;

-- ============================================================================
-- FUNCTIONS for Data Analysis
-- ============================================================================

-- Get latest crawl for a domain
CREATE OR REPLACE FUNCTION get_latest_crawl(domain TEXT)
RETURNS TABLE (
  url TEXT,
  status_code INTEGER,
  title TEXT,
  description TEXT,
  word_count INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.url,
    p.status_code,
    p.title,
    p.description,
    p.word_count
  FROM seo_crawl_pages p
  WHERE p.source_domain = domain
    AND p.crawl_timestamp = (
      SELECT MAX(crawl_timestamp)
      FROM seo_crawl_pages
      WHERE source_domain = domain
    );
END;
$$ LANGUAGE plpgsql;

-- Compare two crawls
CREATE OR REPLACE FUNCTION compare_crawls(
  domain TEXT,
  crawl1 TIMESTAMPTZ,
  crawl2 TIMESTAMPTZ
)
RETURNS TABLE (
  url TEXT,
  change_type TEXT,
  old_status INTEGER,
  new_status INTEGER,
  old_title TEXT,
  new_title TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COALESCE(p1.url, p2.url) as url,
    CASE 
      WHEN p1.url IS NULL THEN 'New Page'
      WHEN p2.url IS NULL THEN 'Removed Page'
      WHEN p1.title != p2.title THEN 'Title Changed'
      WHEN p1.status_code != p2.status_code THEN 'Status Changed'
      ELSE 'No Change'
    END as change_type,
    p1.status_code as old_status,
    p2.status_code as new_status,
    p1.title as old_title,
    p2.title as new_title
  FROM 
    (SELECT * FROM seo_crawl_pages WHERE source_domain = domain AND crawl_timestamp = crawl1) p1
  FULL OUTER JOIN 
    (SELECT * FROM seo_crawl_pages WHERE source_domain = domain AND crawl_timestamp = crawl2) p2
  ON p1.url = p2.url
  WHERE p1.url IS NULL 
     OR p2.url IS NULL 
     OR p1.title != p2.title 
     OR p1.status_code != p2.status_code;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS for Automation
-- ============================================================================

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.created_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_seo_crawl_timestamp
BEFORE INSERT ON seo_crawl_pages
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- ============================================================================
-- DATA RETENTION (Optional)
-- ============================================================================

-- Function to clean old crawl data (keep last N crawls per domain)
CREATE OR REPLACE FUNCTION cleanup_old_crawls(keep_count INTEGER DEFAULT 10)
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  WITH crawls_to_keep AS (
    SELECT DISTINCT ON (source_domain)
      source_domain,
      crawl_timestamp
    FROM seo_crawl_pages
    ORDER BY source_domain, crawl_timestamp DESC
    LIMIT keep_count
  )
  DELETE FROM seo_crawl_pages
  WHERE (source_domain, crawl_timestamp) NOT IN (
    SELECT source_domain, crawl_timestamp FROM crawls_to_keep
  );
  
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-old-crawls', '0 0 * * 0', 'SELECT cleanup_old_crawls(10)');

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Find all 404 errors
-- SELECT url, crawl_timestamp FROM seo_crawl_pages WHERE status_code = 404;

-- Find pages without titles
-- SELECT url, status_code FROM seo_crawl_pages WHERE title IS NULL OR title = '';

-- Get crawl history for a domain
-- SELECT crawl_timestamp, COUNT(*) as pages FROM seo_crawl_pages 
-- WHERE source_domain = 'https://bs-company.ch'
-- GROUP BY crawl_timestamp ORDER BY crawl_timestamp DESC;

-- Find thin content pages
-- SELECT url, word_count FROM seo_crawl_pages 
-- WHERE word_count < 300 AND status_code = 200
-- ORDER BY word_count ASC;

-- Full-text search in titles
-- SELECT url, title FROM seo_crawl_pages 
-- WHERE to_tsvector('english', title) @@ to_tsquery('english', 'SEO & optimization');

-- ============================================================================
-- GRANT PERMISSIONS (Adjust as needed)
-- ============================================================================

-- Grant to service role (already has access via RLS)
GRANT ALL ON seo_crawl_pages TO service_role;
GRANT ALL ON seo_crawl_pages_id_seq TO service_role;

-- Grant to authenticated users
GRANT SELECT, INSERT ON seo_crawl_pages TO authenticated;
GRANT USAGE ON seo_crawl_pages_id_seq TO authenticated;

-- Grant on views
GRANT SELECT ON latest_crawls TO authenticated;
GRANT SELECT ON pages_with_issues TO authenticated;
GRANT SELECT ON status_summary TO authenticated;
GRANT SELECT ON seo_health_scores TO authenticated;

-- ============================================================================
-- COMMENTS for Documentation
-- ============================================================================

COMMENT ON TABLE seo_crawl_pages IS 'Stores crawl data from Screaming Frog SEO Spider';
COMMENT ON COLUMN seo_crawl_pages.url IS 'Full URL of the crawled page';
COMMENT ON COLUMN seo_crawl_pages.source_domain IS 'Base domain that was crawled';
COMMENT ON COLUMN seo_crawl_pages.status_code IS 'HTTP status code (200, 404, 301, etc.)';
COMMENT ON COLUMN seo_crawl_pages.title IS 'Page title from <title> tag';
COMMENT ON COLUMN seo_crawl_pages.description IS 'Meta description content';
COMMENT ON COLUMN seo_crawl_pages.h1 IS 'First H1 heading on page';
COMMENT ON COLUMN seo_crawl_pages.word_count IS 'Number of words in page content';
COMMENT ON COLUMN seo_crawl_pages.indexability IS 'Indexable, Non-Indexable, etc.';
COMMENT ON COLUMN seo_crawl_pages.crawl_timestamp IS 'When this page was crawled';
COMMENT ON COLUMN seo_crawl_pages.meta IS 'Additional metadata in JSON format';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Check table exists
SELECT 'Table created successfully!' as status
WHERE EXISTS (
  SELECT FROM information_schema.tables 
  WHERE table_name = 'seo_crawl_pages'
);

-- Check indexes
SELECT 
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'seo_crawl_pages';

-- Check policies
SELECT 
  policyname,
  cmd,
  qual
FROM pg_policies
WHERE tablename = 'seo_crawl_pages';

-- ============================================================================
-- DONE
-- ============================================================================

-- Your seo_crawl_pages table is ready for Screaming Frog data!
