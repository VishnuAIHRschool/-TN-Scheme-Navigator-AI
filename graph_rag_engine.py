"""
Graph RAG Engine

Default mode:
- Uses local NetworkX fallback from data/tn_scheme_details.csv
- Works without Neo4j AuraDB

Optional mode:
- Uses Neo4j AuraDB only when USE_NEO4J=true is set in .env
"""

import os
from typing import List, Dict

import pandas as pd
import networkx as nx
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = "data/tn_scheme_details.csv"


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def load_scheme_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            "data/tn_scheme_details.csv not found. Run python scrape_schemes.py first."
        )

    df = pd.read_csv(CSV_PATH)
    return df.fillna("")


def build_networkx_graph(df: pd.DataFrame) -> nx.Graph:
    graph = nx.Graph()

    for _, row in df.iterrows():
        scheme = clean(row.get("scheme_title"))
        department = clean(row.get("concerned_department"))
        beneficiary = clean(row.get("beneficiaries"))
        benefit_type = clean(row.get("types_of_benefits"))
        sponsor = clean(row.get("sponsored_by"))

        if not scheme:
            continue

        graph.add_node(scheme, node_type="Scheme")

        relationships = [
            (department, "BELONGS_TO", "Department"),
            (beneficiary, "FOR_BENEFICIARY", "Beneficiary"),
            (benefit_type, "PROVIDES_BENEFIT", "BenefitType"),
            (sponsor, "SPONSORED_BY", "Sponsor"),
        ]

        for target, relation, node_type in relationships:
            if target:
                graph.add_node(target, node_type=node_type)
                graph.add_edge(scheme, target, relation=relation)

    return graph


def detect_query_intent(question: str) -> List[str]:
    q = question.lower()

    keyword_map = {
        "state": ["state", "மாநில"],
        "central": ["central", "மத்திய"],
        "farmer": ["farmer", "farmers", "விவசாயி", "விவசாயிகள்"],
        "grant": ["grant", "grants", "மானியம்"],
        "subsidy": ["subsidy", "மானியம்", "உதவி"],
        "seed": ["seed", "seeds", "விதை"],
        "soil": ["soil", "மண்"],
        "training": ["training", "பயிற்சி"],
        "department": ["department", "துறை"],
    }

    detected = []

    for intent, keywords in keyword_map.items():
        if any(keyword in q or keyword in question for keyword in keywords):
            detected.append(intent)

    return detected


def score_scheme(row: pd.Series, intents: List[str]) -> int:
    combined_text = " ".join(
        [
            clean(row.get("scheme_title")),
            clean(row.get("concerned_department")),
            clean(row.get("beneficiaries")),
            clean(row.get("types_of_benefits")),
            clean(row.get("sponsored_by")),
            clean(row.get("funding_pattern")),
            clean(row.get("description")),
        ]
    ).lower()

    score = 0

    scoring_terms: Dict[str, List[str]] = {
        "state": ["state"],
        "central": ["central"],
        "farmer": ["farmer", "farmers", "agriculture"],
        "grant": ["grant", "grants"],
        "subsidy": ["subsidy"],
        "seed": ["seed", "seeds", "paddy", "maize", "millet"],
        "soil": ["soil", "gypsum", "micronutrient", "micro nutrient"],
        "training": ["training", "demonstration"],
        "department": ["department", "agriculture"],
    }

    for intent in intents:
        for term in scoring_terms.get(intent, []):
            if term in combined_text:
                score += 1

    return score


def ask_graph_ai_local(question: str) -> str:
    df = load_scheme_data()
    graph = build_networkx_graph(df)
    intents = detect_query_intent(question)

    if not intents:
        intents = ["farmer"]

    ranked_rows = []

    for _, row in df.iterrows():
        score = score_scheme(row, intents)
        if score > 0:
            ranked_rows.append((score, row))

    ranked_rows = sorted(ranked_rows, key=lambda item: item[0], reverse=True)[:8]

    if not ranked_rows:
        return (
            "The local NetworkX graph fallback could not find a strong relationship match "
            "for this question from the available scheme data."
        )

    answer_lines = [
        "NetworkX Graph Fallback Answer",
        "",
        f"Graph summary: {graph.number_of_nodes()} nodes and {graph.number_of_edges()} relationships were built locally.",
        "",
        "Relevant schemes found:",
    ]

    for index, (_, row) in enumerate(ranked_rows, start=1):
        scheme = clean(row.get("scheme_title")) or "Untitled Scheme"
        department = clean(row.get("concerned_department")) or "Not available"
        beneficiary = clean(row.get("beneficiaries")) or "Not available"
        benefit = clean(row.get("types_of_benefits")) or "Not available"
        sponsor = clean(row.get("sponsored_by")) or "Not available"
        source = clean(row.get("source_url")) or "Not available"

        answer_lines.append(
            f"""
{index}. {scheme}
   Department: {department}
   Beneficiary: {beneficiary}
   Benefit Type: {benefit}
   Sponsored By: {sponsor}
   Source: {source}
""".strip()
        )

    answer_lines.append(
        "\nNote: This answer was generated using the local NetworkX fallback. "
        "For full Graph RAG, enable Neo4j AuraDB using USE_NEO4J=true."
    )

    return "\n".join(answer_lines)


def ask_graph_ai_neo4j(question: str) -> str:
    from langchain_openai import ChatOpenAI
    from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")

    if not all([neo4j_uri, neo4j_username, neo4j_password]):
        raise ValueError("Neo4j credentials are missing in .env")

    graph = Neo4jGraph(
        url=neo4j_uri,
        username=neo4j_username,
        password=neo4j_password,
        database=neo4j_database,
    )

    graph.refresh_schema()

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


def ask_graph_ai(question: str) -> str:
    """
    Main Graph RAG entry point used by hybrid_rag_engine.py.

    By default, this uses NetworkX fallback so the project runs locally.
    To use Neo4j AuraDB, set USE_NEO4J=true in .env.
    """

    use_neo4j = os.getenv("USE_NEO4J", "false").lower() == "true"

    if use_neo4j:
        try:
            return ask_graph_ai_neo4j(question)
        except Exception as error:
            return (
                f"Neo4j Graph RAG failed, so the app used NetworkX fallback instead.\n\n"
                f"Neo4j error: {error}\n\n"
                f"{ask_graph_ai_local(question)}"
            )

    return ask_graph_ai_local(question)