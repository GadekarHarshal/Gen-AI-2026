
from app.vectorstore import semantic_search


def retrieve_context(question, top_k=5):
    """
    Retrieve the most relevant course information
    from the ChromaDB vector database.
    """

    results = semantic_search(question, top_k=top_k)

    context_parts = []
    sources = []

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        title = metadata.get("title", "Unknown Course")
        source = metadata.get("source", "Unknown Source")

        context_parts.append(
            f"[{index}]\n"
            f"Course: {title}\n"
            f"Source: {source}\n"
            f"Information:\n{result['text']}"
        )

        sources.append({
            "citation": f"[{index}]",
            "title": title,
            "source": source
        })

    return "\n\n".join(context_parts), sources


def generate_rag_answer(question, provider, top_k=5):
    """
    Retrieve relevant information and generate
    a grounded answer using Gemini.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    context, sources = retrieve_context(question, top_k)

    if not context:
        return {
            "answer": "I don't know. The available course information does not contain the answer.",
            "sources": []
        }

    prompt = f"""
You are NPTELPicker, an AI assistant that answers
student questions about NPTEL courses.

YOUR TASK:
Answer the student's question using ONLY the
retrieved context provided below.

STRICT RULES:
1. Do not use outside knowledge.
2. Do not invent course information.
3. If the context does not contain the requested
   information, answer exactly:
   "I don't know. The available course information
   does not contain the answer."
4. Never invent examination dates or examination centres.
5. Never invent credit-transfer policies.
6. Cite supporting information using the citation
   numbers provided, such as [1] or [2].
7. Keep the answer clear and student-friendly.

RETRIEVED CONTEXT:
{context}

STUDENT QUESTION:
{question}

Provide only the answer with relevant citations.
"""

    answer = provider.generate_response(prompt)

    return {
        "answer": answer,
        "sources": sources
    }
