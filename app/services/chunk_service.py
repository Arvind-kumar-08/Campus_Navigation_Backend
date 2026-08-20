def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:

    if not text.strip():
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        candidate = (
            f"{current_chunk}\n{paragraph}".strip()
            if current_chunk
            else paragraph
        )

        if len(candidate) <= chunk_size:
            current_chunk = candidate
            continue

        if current_chunk:
            chunks.append(
                current_chunk.strip()
            )

        # Preserve overlap from previous chunk
        previous_tail = (
            current_chunk[-overlap:]
            if current_chunk
            else ""
        )

        # Move overlap to nearest word boundary
        if previous_tail:
            first_space = previous_tail.find(" ")

            if first_space != -1:
                previous_tail = previous_tail[
                    first_space + 1:
                ]

        current_chunk = (
            f"{previous_tail} {paragraph}"
        ).strip()

        # Very large paragraph fallback
        while len(current_chunk) > chunk_size:

            split_index = current_chunk.rfind(
                " ",
                0,
                chunk_size,
            )

            if split_index == -1:
                split_index = chunk_size

            chunk = current_chunk[
                :split_index
            ].strip()

            chunks.append(chunk)

            start = max(
                0,
                split_index - overlap,
            )

            remaining = current_chunk[
                start:
            ].strip()

            first_space = remaining.find(" ")

            if (
                first_space != -1
                and start > 0
            ):
                remaining = remaining[
                    first_space + 1:
                ]

            current_chunk = remaining

    if current_chunk.strip():
        chunks.append(
            current_chunk.strip()
        )

    return chunks