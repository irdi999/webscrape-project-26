import csv
import time
import re
from urllib.parse import urljoin, quote as url_quote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
START_URL = BASE_URL
OUT_CSV = "output/quotes_with_wiki.csv"

HEADERS = {
    # Wikipedia rekomandon User-Agent unik
    "User-Agent": "quotes-scraper/1.0 (student-project; contact: example@example.com)"
}

def clean_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def scrape_quotes() -> list[dict]:
    """
    Kthen listë me rreshta:
    {quote, author, tags, author_about_url}
    """
    rows = []
    next_url = START_URL

    session = requests.Session()
    session.headers.update(HEADERS)

    while next_url:
        r = session.get(next_url, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for q in soup.select("div.quote"):
            text = q.select_one("span.text")
            author = q.select_one("small.author")
            tags = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]
            about_rel = q.select_one("span a[href^='/author/']")

            if not (text and author):
                continue

            rows.append({
                "quote": clean_whitespace(text.get_text(strip=True)),
                "author": clean_whitespace(author.get_text(strip=True)),
                "tags": ", ".join(tags),
                "author_about_url": urljoin(BASE_URL, about_rel["href"]) if about_rel else ""
            })

        # pagination: link "Next →"
        next_link = soup.select_one("li.next a")
        next_url = urljoin(BASE_URL, next_link["href"]) if next_link else None

    return rows

def fetch_author_wikipedia_summary(author_name: str, session: requests.Session) -> dict:
    """
    Wikipedia REST API: /page/summary/{title}
    Kthen: {wiki_title, wiki_description, wiki_extract, wiki_url}
    Nëse s'gjendet, kthen fusha bosh.
    """
    title = url_quote(author_name.replace(" ", "_"))
    api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

    try:
        r = session.get(api_url, timeout=20)
        if r.status_code != 200:
            return {"wiki_title": "", "wiki_description": "", "wiki_extract": "", "wiki_url": ""}

        data = r.json()
        wiki_title = data.get("title", "") or ""
        wiki_description = data.get("description", "") or ""
        wiki_extract = data.get("extract", "") or ""
        wiki_url = ""
        if isinstance(data.get("content_urls"), dict):
            wiki_url = data["content_urls"].get("desktop", {}).get("page", "") or ""

        return {
            "wiki_title": clean_whitespace(wiki_title),
            "wiki_description": clean_whitespace(wiki_description),
            "wiki_extract": clean_whitespace(wiki_extract),
            "wiki_url": wiki_url
        }
    except Exception:
        return {"wiki_title": "", "wiki_description": "", "wiki_extract": "", "wiki_url": ""}

def save_to_csv(rows: list[dict], path: str) -> None:
    import os
    os.makedirs("output", exist_ok=True)

    fieldnames = [
        "quote", "author", "tags", "author_about_url",
        "wiki_title", "wiki_description", "wiki_extract", "wiki_url"
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    print("1) Duke bërë scraping nga quotes.toscrape.com ...")
    rows = scrape_quotes()
    print(f"   U morën {len(rows)} quotes.")

    print("2) Duke marrë të dhëna shtesë nga Wikipedia API për autorët ...")
    cache = {}  # cache për autorët që përsëriten

    for i, row in enumerate(rows, start=1):
        author = row["author"]
        if author not in cache:
            cache[author] = fetch_author_wikipedia_summary(author, session)
            time.sleep(0.2)  # mos e ngarko API-n kot

        row.update(cache[author])

        if i % 20 == 0:
            print(f"   Përpunuar: {i}/{len(rows)}")

    print("3) Ruajtja në CSV ...")
    save_to_csv(rows, OUT_CSV)
    print(f"   U ruajt: {OUT_CSV}")

if __name__ == "__main__":
    main()
