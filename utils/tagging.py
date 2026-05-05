def generate_tags(text):
    keywords = [
        "AI", "machine learning", "deep learning",
        "health", "data", "NLP", "LLM"
    ]

    tags = []
    text_lower = text.lower()

    for word in keywords:
        if word.lower() in text_lower:
            tags.append(word)

    if not tags:
        tags = ["general"]

    return list(set(tags))