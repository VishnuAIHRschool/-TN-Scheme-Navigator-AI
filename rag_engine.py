from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage

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


def ask_scheme_ai(question: str):
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

    system_prompt = """
You are TN Scheme Advisor AI.

You help users understand Tamil Nadu Government schemes using only the retrieved official scheme context.

Rules:
1. Do not invent any subsidy amount, eligibility, district, process, or document requirement.
2. If the answer is available in the retrieved context, answer clearly.
3. If the answer is not available, say: "This detail is not available in the retrieved scheme information."
4. Always mention the relevant scheme name.
5. Use simple language suitable for farmers and common users.
6. At the end, tell the user to verify the official source link shown below.
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