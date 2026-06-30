import os
from pathlib import Path

import pandas as pd
import pytest
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "tn_scheme_details.csv"


def test_scheme_csv_exists():
    assert CSV_PATH.exists(), "data/tn_scheme_details.csv is missing. Run scrape_schemes.py first."


def test_scheme_csv_has_required_columns():
    df = pd.read_csv(CSV_PATH)

    required_columns = {
        "scheme_title",
        "concerned_department",
        "beneficiaries",
        "types_of_benefits",
        "sponsored_by",
        "description",
        "source_url",
    }

    missing_columns = required_columns - set(df.columns)

    assert not missing_columns, f"Missing required CSV columns: {missing_columns}"
    assert len(df) > 0, "Scheme CSV should contain at least one scheme record."


def test_language_utils_tamil_instruction():
    from language_utils import get_language_instruction

    instruction = get_language_instruction("Tamil")

    assert isinstance(instruction, str)
    assert len(instruction.strip()) > 20
    assert "Tamil" in instruction or "தமிழ்" in instruction


def test_language_utils_ui_keys():
    from language_utils import get_ui_text

    required_keys = {
        "page_title",
        "intro",
        "question_label",
        "placeholder",
        "button",
        "answer_heading",
        "sources_heading",
    }

    for language in ["English", "Tamil", "Bilingual"]:
        ui_text = get_ui_text(language)
        assert required_keys.issubset(ui_text.keys()), f"Missing UI keys for {language}"


def test_hybrid_router_detects_english_relationship_question():
    from hybrid_rag_engine import classify_question

    route = classify_question("Which schemes are sponsored by State?")

    assert route == "hybrid"


def test_hybrid_router_detects_tamil_relationship_question():
    from hybrid_rag_engine import classify_question

    route = classify_question("விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?")

    assert route == "hybrid"


def test_vector_rag_engine_imports():
    from rag_engine import ask_scheme_ai

    assert callable(ask_scheme_ai)


def test_graph_rag_engine_imports():
    from graph_rag_engine import ask_graph_ai

    assert callable(ask_graph_ai)


def test_hybrid_rag_engine_imports():
    from hybrid_rag_engine import ask_hybrid_ai

    assert callable(ask_hybrid_ai)


@pytest.mark.skipif(
    not all([
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD"),
    ]),
    reason="Neo4j credentials not available in environment.",
)
def test_neo4j_connection_read_only():
    from neo4j import GraphDatabase

    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    try:
        with driver.session(database=database) as session:
            result = session.run("MATCH (n) RETURN count(n) AS node_count")
            record = result.single()

            assert record is not None
            assert record["node_count"] >= 0

    finally:
        driver.close()