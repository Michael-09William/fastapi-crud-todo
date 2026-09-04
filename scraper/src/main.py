import os
import re
import requests
import time
import json
from datetime import datetime, timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_DIR = "cache"

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Michael-09William/fastapi-crud-todo)"
}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_page_html(url: str, cache_filename: str) -> str:
    cache_path = os.path.join(CACHE_DIR, cache_filename)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    time.sleep(0.5)

    os.makedirs(CACHE_DIR, exist_ok=True)
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch {url}. Status code: {response.status_code}")

    content = response.text

    # FIX 1: Save using cache_path instead of CACHE_FILE
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def discover_books():
    current_url = BASE_URL
    discovered_items = []
    catalogue_pages_count = 0

    while current_url and catalogue_pages_count < 3:
        catalogue_pages_count += 1
        cache_name = f"catalogue-page-{catalogue_pages_count}.html"
        source_page_url = current_url

        html = get_page_html(current_url, cache_name)
        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            rel_link = article.find("h3").find("a")["href"]

            if rel_link.startswith("../../../"):
                rel_link = rel_link.replace("../../../", "")
            abs_link = urljoin("https://books.toscrape.com/catalogue/", rel_link)

            discovered_items.append({
                "book_url": abs_link,
                "source_page": source_page_url
            })

        next_button = soup.find("li", class_="next")
        if next_button and next_button.find("a"):
            next_rel_path = next_button.find("a")["href"]
            current_url = urljoin(current_url, next_rel_path)
        else:
            current_url = None

    seen = set()
    unique_items = []
    for item in discovered_items:
        if item["book_url"] not in seen:
            seen.add(item["book_url"])
            unique_items.append(item)

    return unique_items


def clean_text(text: str) -> str:
    if not text:
        return None
    fixed = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore") if "Â" in text or "â" in text else text
    return fixed.strip()


def extract_and_clean_book(book_item: dict, index: int) -> dict:
    url = book_item["book_url"]
    source_page = book_item["source_page"]

    cache_filename = f"book-detail-{index + 1}.html"
    html = get_page_html(url, cache_filename)
    soup = BeautifulSoup(html, "html.parser")

    product_main = soup.find("div", class_="product_main")

    title = clean_text(product_main.find("h1").text)

    price_text = product_main.find("p", class_="price_color").text
    price_match = re.search(r"[\d\.]+", price_text)
    price = float(price_match.group()) if price_match else 0.0
    currency = "GBP"

    availability_text = product_main.find("p", class_="instock availability").text.strip()
    stock_match = re.search(r"\d+", availability_text)
    in_stock_count = int(stock_match.group()) if stock_match else 0
    is_available = in_stock_count > 0

    rating_tag = product_main.find("p", class_="star-rating")
    rating_text = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else None
    rating = RATING_MAP.get(rating_text, 0)

    desc_tag = soup.find("div", id="product_description")
    raw_desc = desc_tag.find_next_sibling("p").text.strip() if desc_tag and desc_tag.find_next_sibling("p") else None
    description = clean_text(raw_desc)

    # FIX 2: Return structured & cleaned schema
    return {
        "title": title,
        "product_url": url,
        "price": price,
        "currency": currency,
        "is_available": is_available,
        "in_stock_count": in_stock_count,
        "rating": rating,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }


def run_stage_4():
    books_to_extract = discover_books()
    cleaned_records = []

    for idx, item in enumerate(books_to_extract):
        record = extract_and_clean_book(item, idx)
        cleaned_records.append(record)

    assert len(cleaned_records) == 60, "Expected exactly 60 records"
    assert all(isinstance(r["price"], float) for r in cleaned_records), "Price must be float"
    assert all(1 <= r["rating"] <= 5 for r in cleaned_records), "Rating must be integer 1-5"

    print("--- Sample Cleaned Record ---")
    print(json.dumps(cleaned_records[0], indent=2))
    print(f"valid_cleaned_records = {len(cleaned_records)}")

    return cleaned_records


if __name__ == "__main__":
    run_stage_4()