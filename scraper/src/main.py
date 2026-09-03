import os
import requests
import time
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
    book_urls= []
    catalogue_pages_count= 0

    while current_url and catalogue_pages_count <3:
        catalogue_pages_count +=1
        cache_name= f"catalogue-page-{catalogue_pages_count}.html"

        html = get_page_html(current_url,cache_name)
        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all("article",class_="product_pod")
        for article in articles:
            rel_link = article.find("h3").find("a")["href"]
            abs_link = urljoin(current_url,rel_link)
            book_urls.append(abs_link)

        next_button = soup.find("li",class_="next")
        if next_button and next_button.find("a"):
            next_rel_path = next_button.find("a")["href"]
            current_url=urljoin(current_url,next_rel_path)
        else:
            current_url = None

    unique_urls = list(dict.fromkeys(book_urls))

    print(f"catalogue_pages = {catalogue_pages_count}")
    print(f"discovered = {len(book_urls)}")
    print(f"unique_urls = {len(unique_urls)}")

    return unique_urls

if __name__ == "__main__":
    discover_books()
    