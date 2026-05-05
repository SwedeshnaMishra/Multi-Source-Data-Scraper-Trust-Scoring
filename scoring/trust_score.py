from datetime import datetime


def get_domain_score(url):
    trusted_domains = {
        "nature.com": 0.95,
        "pubmed.ncbi.nlm.nih.gov": 1.0,
        "medium.com": 0.6,
        "analyticsvidhya.com": 0.7,
        "youtube.com": 0.7
    }

    for domain in trusted_domains:
        if domain in url:
            return trusted_domains[domain]

    return 0.3   # penalty for unknown domains


def calculate_recency(published_date):
    try:
        year = int(published_date[:4])
        current_year = datetime.now().year

        if year >= current_year - 1:
            return 1.0
        elif year >= current_year - 3:
            return 0.7
        else:
            return 0.4
    except:
        return 0.3


def calculate_trust_score(data):
    # ---------------- AUTHOR SCORE ----------------
    num_authors = data.get("num_authors", 1)

    if num_authors > 1:
        author_score = 0.9
    elif data["author"] != "unknown":
        author_score = 0.7
    else:
        author_score = 0.3

    # ---------------- CITATION SCORE ----------------
    if data["source_type"] == "pubmed":
        citation_score = 1.0
    elif data["source_type"] == "youtube":
        citation_score = 0.5
    else:
        citation_score = 0.4

    # ---------------- DOMAIN ----------------
    domain_score = get_domain_score(data["source_url"])

    # ---------------- RECENCY ----------------
    recency_score = calculate_recency(data["published_date"])

    # ---------------- MEDICAL DISCLAIMER ----------------
    medical_keywords = [
        "not medical advice",
        "consult a doctor",
        "for educational purposes",
        "medical disclaimer"
    ]

    content_text = " ".join(data["content_chunks"]).lower()

    disclaimer_score = 1.0 if any(k in content_text for k in medical_keywords) else 0.3

    # ---------------- FINAL SCORE ----------------
    trust = (
        0.25 * author_score +
        0.20 * citation_score +
        0.20 * domain_score +
        0.20 * recency_score +
        0.15 * disclaimer_score
    )

    trust = max(0, min(1, trust))

    return round(trust, 2)