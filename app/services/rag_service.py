from groq import Groq
from sqlmodel import Session

from app.core.config import settings
from app.models.document import Document
from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)


client = Groq(
    api_key=settings.GROQ_API_KEY,
)


GENERATION_MODEL = "llama-3.3-70b-versatile"


def generate_rag_answer(
    session: Session,
    question: str,
) -> dict:

    # -----------------------------------------
    # 1. Retrieve relevant chunks
    # -----------------------------------------

    retrieved = retrieve_relevant_chunks(
        session=session,
        question=question,
        top_k=5,
    )

    # -----------------------------------------
    # 2. No relevant context
    # -----------------------------------------

    if not retrieved:
        return {
            "question": question,
            "answer": (
                "I could not find this information "
                "in the current RGIPT knowledge base."
            ),
            "sources": [],
            "retrieved_chunks": 0,
        }

    # -----------------------------------------
    # 3. Prepare RAG context
    # -----------------------------------------

    context_parts = []

    sources = []

    seen_sources = set()

    for index, result in enumerate(
        retrieved,
        start=1,
    ):
        chunk, distance = result

        document = session.get(
            Document,
            chunk.document_id,
        )

        if document:
            document_name = (
                document.filename.strip()
            )
        else:
            document_name = (
                "Unknown document"
            )

        page_number = (
            chunk.page_number
        )

        # -------------------------------------
        # Add chunk to LLM context
        # -------------------------------------

        context_parts.append(
            f"""
SOURCE {index}

Document: {document_name}
Page: {page_number}

{chunk.content}
""".strip()
        )

        # -------------------------------------
        # Deduplicate sources
        #
        # Same document + same page
        # should only appear once.
        # -------------------------------------

        source_key = (
            document_name
            .strip()
            .lower(),
            page_number,
        )

        if source_key not in seen_sources:

            seen_sources.add(
                source_key
            )

            sources.append(
                {
                    "document":
                        document_name,

                    "page":
                        page_number,
                }
            )

    # -----------------------------------------
    # 4. Build final context
    # -----------------------------------------

    context = "\n\n".join(
        context_parts
    )

    # -----------------------------------------
    # 5. System prompt
    # -----------------------------------------

    system_prompt = """
You are the official AI guide for RGIPT
(Rajiv Gandhi Institute of Petroleum Technology).

Your job is to answer questions using ONLY the
RGIPT information provided in the context.

Rules:

1. Do not invent institute-specific facts.

2. If the answer is not present in the supplied
   RGIPT context, clearly say that the information
   is not available in the current RGIPT knowledge
   base.

3. Do not use general knowledge to answer
   institute-specific questions.

4. Keep answers clear, concise, and helpful.

5. Only mention institute rules, policies,
   facilities, timings, fees, procedures, or
   disciplinary actions if they are supported
   by the provided context.

6. If multiple relevant pieces of information
   exist, combine them into one clear answer.

7. Do not mention RAG, embeddings, vector search,
   cosine similarity, chunks, database queries,
   or any internal backend implementation.

8. Do not create fake document names or page
   numbers.

9. The source information will be handled by the
   backend separately, so do not add a separate
   Sources section inside your answer.
""".strip()

    # -----------------------------------------
    # 6. User prompt
    # -----------------------------------------

    user_prompt = f"""
RGIPT CONTEXT:

{context}


USER QUESTION:

{question}
""".strip()

    # -----------------------------------------
    # 7. Generate answer using Groq
    # -----------------------------------------

    try:

        response = (
            client.chat.completions.create(
                model=GENERATION_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content":
                            system_prompt,
                    },
                    {
                        "role": "user",
                        "content":
                            user_prompt,
                    },
                ],

                temperature=0.2,

                max_tokens=700,
            )
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        if answer:
            answer = answer.strip()

        else:
            answer = (
                "I could not generate an "
                "answer from the available "
                "RGIPT information."
            )

    except Exception as error:

        print(
            "Groq generation error:",
            error,
        )

        raise RuntimeError(
            "AI service is temporarily "
            "unavailable."
        ) from error

    # -----------------------------------------
    # 8. Final safety deduplication
    # -----------------------------------------

    unique_sources = []

    final_seen_sources = set()

    for source in sources:

        source_key = (
            source["document"]
            .strip()
            .lower(),

            source["page"],
        )

        if (
            source_key
            not in final_seen_sources
        ):

            final_seen_sources.add(
                source_key
            )

            unique_sources.append(
                source
            )

    # -----------------------------------------
    # 9. Return final API response
    # -----------------------------------------

    return {
        "question":
            question,

        "answer":
            answer,

        "sources":
            unique_sources,

        "retrieved_chunks":
            len(retrieved),
    }