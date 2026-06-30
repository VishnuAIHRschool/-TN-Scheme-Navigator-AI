from langchain_openai import ChatOpenAI

from rag_engine import ask_scheme_ai
from graph_rag_engine import ask_graph_ai
from language_utils import get_language_instruction


def classify_question(question: str) -> str:
    """
    Smart router:
    Decides whether the user question needs vector search, graph search, or both.
    """

    question_lower = question.lower()

    graph_keywords = [
        "sponsored",
        "sponsor",
        "state",
        "central",
        "department",
        "beneficiary",
        "beneficiaries",
        "farmer",
        "farmers",
        "grant",
        "subsidy",
        "benefit",
        "scheme type",
        "connected",
        "relationship",
        "belongs to",
        "under",
        "linked",
        "provide",
        "provides",
    ]

    tamil_graph_keywords = [
        "மாநில",
        "மத்திய",
        "துறை",
        "விவசாயி",
        "விவசாயிகள்",
        "மானியம்",
        "உதவி",
        "நிதி",
        "பயனாளி",
        "திட்டம்",
        "சார்ந்த",
        "வழங்கும்",
    ]

    if any(keyword in question_lower for keyword in graph_keywords):
        return "hybrid"

    if any(keyword in question for keyword in tamil_graph_keywords):
        return "hybrid"

    return "vector"


def build_source_text(sources):
    """
    Converts source list into readable context for final answer.
    """

    if not sources:
        return "No official sources returned."

    source_lines = []

    for index, source in enumerate(sources, start=1):
        source_lines.append(f"Source {index}: {source}")

    return "\n".join(source_lines)


def ask_hybrid_ai(question: str, language: str = "English"):
    """
    Next-level Hybrid RAG:
    - Uses smart routing
    - Uses ChromaDB Vector RAG
    - Uses Neo4j Graph RAG when needed
    - Produces final answer in English, Tamil, or bilingual format
    """

    route = classify_question(question)

    vector_answer = ""
    graph_answer = ""
    vector_sources = []

    try:
        vector_answer, vector_sources = ask_scheme_ai(question)
    except Exception as error:
        vector_answer = f"Vector RAG could not run. Error: {error}"

    if route == "hybrid":
        try:
            graph_answer = ask_graph_ai(question)
        except Exception as error:
            graph_answer = f"Graph RAG could not run. Error: {error}"
    else:
        graph_answer = "Graph RAG was not required for this question."

    language_instruction = get_language_instruction(language)
    source_text = build_source_text(vector_sources)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
    )

    final_prompt = f"""
You are TN Scheme Navigator AI, an expert assistant for Tamil Nadu Government schemes.

User question:
{question}

Selected response language:
{language}

Language instruction:
{language_instruction}

Routing decision:
{route}

Vector RAG answer:
{vector_answer}

Graph RAG answer:
{graph_answer}

Official source references:
{source_text}

Create a final high-quality answer.

Rules:
1. Answer only using the provided Vector RAG and Graph RAG information.
2. Do not invent scheme details.
3. If information is not available, say clearly that the available data does not confirm it.
4. Mention scheme names clearly.
5. Explain:
   - Suitable schemes
   - Beneficiaries
   - Benefits
   - Sponsor or department if available
   - How to apply if available
6. Keep the answer simple and citizen-friendly.
7. Add a short note reminding the user to verify from the official source link.
"""

    final_response = llm.invoke(final_prompt)

    return final_response.content, vector_sources, route