-- Minimal tables for storing reports
create table if not exists public.seo_reports (
  id text primary key,
  payload jsonb not null,
  created_at timestamp with time zone default now()
);
