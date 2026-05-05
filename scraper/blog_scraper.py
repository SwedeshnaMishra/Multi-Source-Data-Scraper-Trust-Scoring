import requests
from bs4 import BeautifulSoup
from datetime import datetime

from utils.chunking import chunk_text
from utils.language import detect_language
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score

def scrape_blog(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # TITLE
    title = soup.title.string.strip() if soup.title else ""
    if "|" in title:
        title = title.split("|")[0].strip()

    # DESCRIPTION
    description = ""
    desc_tag = soup.find("meta", {"name": "description"})
    if desc_tag:
        description = desc_tag.get("content")

    # AUTHOR
    author = ""
    author_tag = soup.find("meta", {"name": "author"})
    if author_tag:
        author = author_tag.get("content")

    if not author:
        author_tag = soup.find("meta", {"property": "og:site_name"})
        if author_tag:
            author = author_tag.get("content")

    # DATE
    date = ""
    date_tag = soup.find("meta", {"property": "article:published_time"})
    if date_tag:
        date = date_tag.get("content")

    # CONTENT
    article = soup.find("article")
    if article:
        paragraphs = article.find_all("p")
    else:
        paragraphs = soup.select("div p")

    content = " ".join([
        p.get_text().strip()
        for p in paragraphs
        if len(p.get_text().strip()) > 50
    ])

    if not content or len(content.strip()) == 0:
        content = description if description else title

    # LANGUAGE
    language = detect_language(content)

    # FALLBACK
    author = author if author else "unknown"
    date = date if date else "unknown"
    language = language if language else "unknown"

    # FORMAT DATE
    try:
        if date != "unknown":
            date = datetime.fromisoformat(date.replace("Z", "")).strftime("%Y-%m-%d")
    except:
        pass

    # REGION
    region = "global" if "medium.com" in url else "unknown"

    # TAGGING
    tags = generate_tags(content)
    if not tags:
        tags = ["general"]

    # CHUNKING
    chunks = chunk_text(content, size=80)

    # FINAL DATA
    data = {
        "source_url": url,
        "source_type": "blog",
        "title": title,
        "description": description,
        "author": author,
        "published_date": date,
        "language": language,
        "region": region,
        "topic_tags": tags,
        "content_chunks": chunks
    }

    data["trust_score"] = calculate_trust_score(data)

    return data