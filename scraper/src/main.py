import os
import requests
import time
import json
from datetime import datetime, timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue-page-1.html")


HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Michael-09William/fastapi-crud-todo)"
}


def get_page_html(url: str , cache_filename: str)->str:

    cache_path = os.path.join(CACHE_DIR,cache_filename)

    if os.path.exists(cache_path):
        with open(cache_path,"r",encoding="utf-8") as f:
            content = f.read()
        #print(f"CACHE HIT | Response size: {len(content)} bytes")
        return content

    time.sleep(0.5)


    os.makedirs(CACHE_DIR, exist_ok=True)
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch page. Status code: {response.status_code}")

    content = response.text

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"FETCH | Response size: {len(content)} bytes")
    return content

def discover_books():

    current_url= BASE_URL
    discovered_items= []
    catalogue_pages_count= 0

    while current_url and catalogue_pages_count <3:
        catalogue_pages_count +=1
        cache_name= f"catalogue-page-{catalogue_pages_count}.html"
        source_page_url = current_url

        html = get_page_html(current_url,cache_name)
        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all("article",class_="product_pod")
        for article in articles:
            rel_link = article.find("h3").find("a")["href"]
            abs_link = urljoin(current_url,rel_link)
            discovered_items.append({"book_url":abs_link,
                              "source_page":source_page_url})


        next_button = soup.find("li",class_="next")
        if next_button and next_button.find("a"):
            next_rel_path = next_button.find("a")["href"]
            current_url=urljoin(current_url,next_rel_path)
        else:
            current_url = None
    seen = set()
    unique_items = []
    for item in discovered_items:
        if item["book_url"] not in seen:
            seen.add(item["book_url"])
            unique_items.append(item)

    return unique_items


def extract_book_details(book_item: dict, index: int) -> dict:
    url = book_item["book_url"]
    source_page = book_item["source_page"]
    
    cache_filename = f"book-detail-{index + 1}.html"
    html = get_page_html(url, cache_filename)
    soup = BeautifulSoup(html, "html.parser")

    product_main = soup.find("div", class_="product_main")
    
    title = product_main.find("h1").text.strip()
    price_text = product_main.find("p", class_="price_color").text.strip()
    availability_text = product_main.find("p", class_="instock availability").text.strip()
    
    rating_tag = product_main.find("p", class_="star-rating")
    rating_text = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else None

    desc_tag = soup.find("div", id="product_description")
    description = desc_tag.find_next_sibling("p").text.strip() if desc_tag and desc_tag.find_next_sibling("p") else None

    return {
        "title": title,
        "product_url": url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

def run_extracting():
    books_to_extract = discover_books()
    raw_records = []

    for idx, item in enumerate(books_to_extract):
        record = extract_book_details(item, idx)
        raw_records.append(record)

    print("--- Sample Raw Record ---")
    print(json.dumps(raw_records[0], indent=2))
    print(f"detail_pages = {len(raw_records)}")
    
    return raw_records

if __name__ == "__main__":
    run_extracting()
    