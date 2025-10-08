# n8n Workflow (Example)

- Create a cron trigger (e.g., weekly).
- Add HTTP Request node:
  - Method: POST
  - URL: {{API_BASE_URL}}/webhooks/scan
  - Body: { "websiteId": "site-123", "url": "https://example.com" }
- Add Email node to send summary.
