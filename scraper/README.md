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

### Stage 2: Discover Three Catalogue Pages
- **Dynamic Crawling:** Discovers book pages by following pagination `next` buttons dynamically up to 3 catalogue pages max.
- **URL Resolution:** Converts relative links (e.g., `../book-name/index.html`) to absolute URLs using standard URL tools (`urljoin`)[cite: 1].
- **Politeness & Rate-Limiting:** Enforces a minimum delay of 500ms between real network requests[cite: 1].
- **Deduplication:** Removes duplicate links to ensure exactly 60 unique book URLs[cite: 1].

### Stage 3: Extract Raw Records
- **Detail Extraction:** Visits all 60 individual book pages and extracts raw text fields (title, price_text, availability_text, rating_text, and description).
- **Null Handling:** Stores `null` when a description is missing on the source page without fabricating text[cite: 1].
- **Data Provenance:** Attaches `source_page` URL and UTC `fetched_at` timestamp to every extracted record for tracking[cite: 1].

## Stage 4: Data Cleaning, Parsing & Type Conversion

### Objective
Process and clean the extracted raw web data into a fully typed, normalized, and structured schema ready for downstream storage and analysis.

---

### Implementation Details

* **Numeric Extraction & Conversion**: Extracted float values for product prices and integer values for stock availability using regular expressions (`re`).
* **Text Normalization**: Cleaned encoding anomalies (such as UTF-8/Latin-1 artifacts like `Â`) and trimmed whitespace from titles and descriptions.
* **Rating Mapping**: Transformed string-based star ratings (`One`, `Two`, `Three`, `Four`, `Five`) into integer values ranging from `1` to `5`.
* **Boolean Flagging**: Standardized `is_available` as a boolean flag based on in-stock unit count.
* **Metadata Normalization**: Captured ISO 8601 UTC timestamps (`fetched_at`) and standard currency codes (`GBP`).

---

### Validation & Output

The stage pipeline verifies the processed records through strict assertions:

* Total valid records extracted: **60**
* Price data type check: `float`
* Rating bounds check: `1 <= rating <= 5`

#### Sample Cleaned Record Schema

```json
{
  "title": "A Light in the Attic",
  "product_url": "[https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html](https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html)",
  "price": 51.77,
  "currency": "GBP",
  "is_available": true,
  "in_stock_count": 22,
  "rating": 3,
  "description": "It's hard to be a book lover...",
  "source_page": "[https://books.toscrape.com/catalogue/page-1.html](https://books.toscrape.com/catalogue/page-1.html)",
  "fetched_at": "2026-09-05T00:00:00+00:00"}
  ```

## Stage 5: Data Persistence & Export Pipeline

### Objective
Persist normalized and cleaned datasets into standard structured formats (`JSON` and `CSV`) in the designated output directory while ensuring character encoding integrity and dataset completeness.

---

### Implementation Details

* **Directory Setup**: Automated creation of the output directory (`data/`) using `os.makedirs`.
* **JSON Export**: Exported cleaned book dict objects using `json.dump` with formatting (`indent=2`) and `ensure_ascii=False` to preserve special text characters.
* **CSV Export**: Utilized Python's `csv.DictWriter` to dynamic-map header fieldnames and export rows accurately with `utf-8` encoding.

---

### Validation & Verification

* **Output Files Generated**:
  * `data/books.json`
  * `data/books.csv`
* **Assertions Checks**:
  * Output files exist on disk.
  * Both generated files contain non-zero bytes (`os.path.getsize > 0`).
  * Record count parity checked (60 records in both JSON & CSV).