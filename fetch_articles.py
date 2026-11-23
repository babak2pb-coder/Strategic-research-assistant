import requests
from bs4 import BeautifulSoup


SOURCES = {
    "Foreign Affairs": "https://www.foreignaffairs.com/",
    "Foreign Policy": "https://foreignpolicy.com/",
    "INSS": "https://www.inss.org.il/"
}


def fetch_articles(source_name, url):
    print(f"\nChecking {source_name}...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a", href=True)

        articles = []

        for link in links:
            title = link.get_text(" ", strip=True)
            article_url = link["href"]

            if title and len(title) > 30:
                if article_url.startswith("/"):
                    article_url = url.rstrip("/") + article_url

                if article_url.startswith("http"):
                    articles.append({
                        "source": source_name,
                        "title": title,
                        "url": article_url
                    })

        return articles

    except requests.RequestException as error:
        print(f"Error: {error}")
        return []


def main():
    all_articles = []

    for source_name, url in SOURCES.items():
        articles = fetch_articles(source_name, url)
        all_articles.extend(articles)

    print(f"\nTotal articles found: {len(all_articles)}")

    for article in all_articles[:10]:
        print("\nSource:", article["source"])
        print("Title:", article["title"])
        print("URL:", article["url"])


if __name__ == "__main__":
    main()