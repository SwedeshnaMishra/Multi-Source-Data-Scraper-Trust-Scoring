def chunk_text(text, size=80):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        if len(chunk.strip()) > 100:   
            chunks.append(chunk)

    return chunks