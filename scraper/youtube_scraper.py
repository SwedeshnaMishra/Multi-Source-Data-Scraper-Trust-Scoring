import yt_dlp
import re
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

from utils.chunking import chunk_text
from utils.language import detect_language
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score


def get_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[1]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    return ""


def clean_transcript(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
    except:
        return "unknown"


def scrape_youtube(url):
    ydl_opts = {"quiet": True, "skip_download": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get("title", "")
    author = info.get("channel", "")
    published_date = format_date(info.get("upload_date", ""))
    description = info.get("description", "")

    video_id = get_video_id(url)
    transcript_text = ""

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        raw = " ".join([t["text"] for t in transcript])
        transcript_text = clean_transcript(raw)
    except:
        transcript_text = ""

    if not transcript_text:
        transcript_text = description if description else title

    language = detect_language(transcript_text)

    # FALLBACK
    author = author if author else "unknown"
    published_date = published_date if published_date else "unknown"
    language = language if language else "unknown"

    region = "global"

    tags = generate_tags(transcript_text)
    if not tags:
        tags = ["general"]

    chunks = chunk_text(transcript_text, size=80)

    data = {
        "source_url": url,
        "source_type": "youtube",
        "title": title,
        "description": description,
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": region,
        "topic_tags": tags,
        "content_chunks": chunks
    }

    data["trust_score"] = calculate_trust_score(data)

    return data