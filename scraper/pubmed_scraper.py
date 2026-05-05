from Bio import Entrez

from utils.chunking import chunk_text
from utils.language import detect_language
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score

Entrez.email = "swedeshnamishra364@gmail.com"


def scrape_pubmed(pmid):
    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    records = Entrez.read(handle)

    article = records["PubmedArticle"][0]["MedlineCitation"]["Article"]

    title = article.get("ArticleTitle", "")

    authors_list = article.get("AuthorList", [])
    authors = []
    for a in authors_list:
        if "LastName" in a and "ForeName" in a:
            authors.append(a["ForeName"] + " " + a["LastName"])

    author = ", ".join(authors)

    journal = article["Journal"]["Title"]

    pub_date = article["Journal"]["JournalIssue"]["PubDate"]
    year = pub_date.get("Year", "unknown")

    abstract = ""
    if "Abstract" in article:
        abstract = " ".join(article["Abstract"]["AbstractText"])

    if not abstract:
        abstract = title

    language = detect_language(abstract)

    # FALLBACK
    author = author if author else "unknown"
    year = year if year else "unknown"
    language = language if language else "unknown"

    region = "global"

    tags = generate_tags(abstract)
    if not tags:
        tags = ["medical", "research"]

    chunks = chunk_text(abstract, size=80)

    # NEW: number of authors
    num_authors = len(authors_list)

    data = {
        "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "source_type": "pubmed",
        "title": title,
        "description": abstract[:300],
        "author": author,
        "published_date": year,
        "language": language,
        "region": region,
        "topic_tags": tags,
        "content_chunks": chunks,
        "num_authors": num_authors   
    }

    data["trust_score"] = calculate_trust_score(data)

    return data