import json
import os
import time

from scraper.blog_scraper import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed

start = time.time()

os.makedirs("output", exist_ok=True)

# ---------------- BLOG ----------------
blog_urls = [
    "https://medium.com/%40securedhummer/starting-my-first-machine-learning-project-and-my-first-blog-post-in-forever-c13d6617a2f0",
    "https://www.analyticsvidhya.com/blog/2021/05/natural-language-processing-step-by-step-guide/",
    "https://medium.com/analytics-vidhya/natural-language-processing-nlp-introduction-fe48e9b7ec8d"
]

blog_data = []

for url in blog_urls:
    try:
        data = scrape_blog(url)
        blog_data.append(data)
    except Exception as e:
        print(f"Error scraping blog {url}: {e}")

with open("output/blogs.json", "w") as f:
    json.dump(blog_data, f, indent=4)


# ---------------- YOUTUBE ----------------
youtube_urls = [
    "https://www.youtube.com/watch?v=aircAruvnKk",
    "https://www.youtube.com/watch?v=ua-CiDNNj30"
]

youtube_data = []

for url in youtube_urls:
    try:
        data = scrape_youtube(url)
        youtube_data.append(data)
    except Exception as e:
        print(f"Error scraping YouTube {url}: {e}")

with open("output/youtube.json", "w") as f:
    json.dump(youtube_data, f, indent=4)


# ---------------- PUBMED ----------------
pubmed_ids = [
    "31452104"
]

pubmed_data = []

for pmid in pubmed_ids:
    try:
        data = scrape_pubmed(pmid)
        pubmed_data.append(data)
    except Exception as e:
        print(f"Error scraping PubMed {pmid}: {e}")

with open("output/pubmed.json", "w") as f:
    json.dump(pubmed_data, f, indent=4)


# ---------------- COMBINED ----------------
combined_data = blog_data + youtube_data + pubmed_data

with open("output/scraped_data.json", "w") as f:
    json.dump(combined_data, f, indent=4)


# ---------------- LOGS ----------------
print(f"Blogs scraped: {len(blog_data)}")
print(f"YouTube videos scraped: {len(youtube_data)}")
print(f"PubMed articles scraped: {len(pubmed_data)}")
print("All data saved successfully!")

end = time.time()
print(f"Execution time: {round(end - start, 2)} seconds")