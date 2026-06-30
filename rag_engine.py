from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage

from language_utils import get_language_instruction

load_dotenv()

DB_PATH = "vector_db"
COLLECTION_NAME = "tn_scheme_details"


def get_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def ask_scheme_ai(question: str, language: str = "English"):
    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )

    language_instruction = get_language_instruction(language)

    system_prompt = f"""
You are TN Scheme Advisor AI, a citizen service assistant for Tamil Nadu Government schemes
(MSME owners, entrepreneurs, students, women entrepreneurs, rural businesses, and first-time applicants).

You help users understand schemes using only the retrieved official scheme context below.

Grounding rules:
1. Do not invent any subsidy amount, eligibility, district, process, or document requirement.
2. Use only facts present in the retrieved context. If a detail is missing, say:
   "This detail is not available in the retrieved scheme information."
3. Always mention the relevant scheme name(s) explicitly.

Answer quality rules:
4. If the question is vague or could match many schemes (e.g. just "schemes" or "help"),
   ask one short clarifying question (e.g. about sector, beneficiary type, or district)
   instead of guessing, unless the retrieved context already makes the right scheme obvious.
5. When eligibility, benefits, required documents, or application process are present in the
   context, structure the answer under those headings.
6. Use simple, plain language suitable for first-time applicants, not legal/bureaucratic phrasing.
7. End by reminding the user to verify details from the official source link shown below.

Language instruction:
{language_instruction}
"""

    user_prompt = f"""
User Question:
{question}

Retrieved Scheme Context:
{context}

Now answer the user clearly.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    sources = []

    for doc in docs:
        sources.append({
            "scheme_title": doc.metadata.get("scheme_title", ""),
            "department": doc.metadata.get("department", ""),
            "beneficiaries": doc.metadata.get("beneficiaries", ""),
            "benefit_type": doc.metadata.get("benefit_type", ""),
            "source_url": doc.metadata.get("source_url", ""),
        })

    return response.content, sources