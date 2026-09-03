# Polite Book Scraper - FlyRank Internship (A9)

## Target Classification

- **Target Site:** [Books to Scrape](https://books.toscrape.com/) (A practice sandbox built specifically for scraping practice).
- **Scope:** First 3 catalogue pages only (total of 60 unique books).
- **Data Collected:** Title, Product URL, Price (GBP), Availability, Rating, Description, Source Page, and Timestamp.
- **Robots.txt Check:** `no robots file found` (HTTP 404).
- **Ethics & Rules:** I will not reuse this code on another site without checking its rules and terms first.

---

## Features & Implementation Progress

### Stage 1: Fetch Once, Cache Once
- **Polite Requests:** Included identification header (`User-Agent`) with repository link and set network timeouts (10s).
- **Caching Mechanism:** Saves downloaded HTML files to `cache/` directory. Reads directly from disk on subsequent runs (`CACHE HIT`), minimizing server strain.
- **Error Handling:** Validates HTTP status code (`200 OK`) before attempting to process HTML content.
- **Status Reporting:** Logs output status (`FETCH` or `CACHE HIT`) alongside the exact response size in bytes without dumping raw HTML into the console.