import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def get_neo4j_graph():
    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        raise ValueError("Neo4j environment variables are missing. Please check your .env file.")

    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database=NEO4J_DATABASE,
    )

    graph.refresh_schema()
    return graph


def ask_graph_ai(question: str):
    graph = get_neo4j_graph()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
    )

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        validate_cypher=True,
        allow_dangerous_requests=True,
        top_k=10,
    )

    response = chain.invoke({"query": question})

    return response.get("result", "No graph answer generated.")