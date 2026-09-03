import os
import requests

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue-page-1.html")


HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Michael-09William/fastapi-crud-todo)"
}


def fetch_and_cache_stage1():

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE,"r",encoding="utf-8") as f:
            content = f.read()
        print(f"CACHE HIT | Response size: {len(content)} bytes")
        return content

    os.makedirs(CACHE_DIR, exist_ok=True)
    response = requests.get(BASE_URL, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch page. Status code: {response.status_code}")

    content = response.text

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"FETCH | Response size: {len(content)} bytes")
    return content

if __name__ == "__main__":
    fetch_and_cache_stage1()
    