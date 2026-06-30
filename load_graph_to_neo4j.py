import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

CSV_PATH = "data/tn_scheme_details.csv"

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def run_write(session, query, params=None):
    if params is None:
        params = {}

    def work(tx):
        result = tx.run(query, **params)
        result.consume()

    session.execute_write(work)


def create_constraints(session):
    constraints = [
        "CREATE CONSTRAINT scheme_name IF NOT EXISTS FOR (s:Scheme) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT department_name IF NOT EXISTS FOR (d:Department) REQUIRE d.name IS UNIQUE",
        "CREATE CONSTRAINT beneficiary_name IF NOT EXISTS FOR (b:Beneficiary) REQUIRE b.name IS UNIQUE",
        "CREATE CONSTRAINT benefit_name IF NOT EXISTS FOR (bt:BenefitType) REQUIRE bt.name IS UNIQUE",
        "CREATE CONSTRAINT sponsor_name IF NOT EXISTS FOR (sp:Sponsor) REQUIRE sp.name IS UNIQUE",
        "CREATE CONSTRAINT keyword_name IF NOT EXISTS FOR (k:Keyword) REQUIRE k.name IS UNIQUE",
    ]

    for query in constraints:
        run_write(session, query)


def get_keywords(row):
    text = " ".join([
        clean(row.get("scheme_title")),
        clean(row.get("description")),
        clean(row.get("types_of_benefits")),
        clean(row.get("funding_pattern")),
        clean(row.get("beneficiaries")),
    ]).lower()

    keyword_map = {
        "Seed Support": ["seed", "seeds", "paddy", "maize", "millet", "cotton"],
        "Training": ["training", "demonstration"],
        "Soil Health": ["soil", "gypsum", "micro nutrient", "micronutrient"],
        "Pest Management": ["pest", "plant protection", "virus", "ipm"],
        "Water Support": ["pipe", "water", "irrigation"],
        "Grant": ["grant", "grants"],
        "Subsidy": ["subsidy"],
        "Farmer Support": ["farmer", "farmers", "agriculture"],
        "Livelihood": ["livelihood", "asset less"],
    }

    matched_keywords = []

    for keyword, terms in keyword_map.items():
        if any(term in text for term in terms):
            matched_keywords.append(keyword)

    return matched_keywords


def create_scheme_graph(session, row):
    scheme_title = clean(row.get("scheme_title"))

    if not scheme_title:
        return

    params = {
        "scheme_title": scheme_title,
        "department": clean(row.get("concerned_department")),
        "beneficiaries": clean(row.get("beneficiaries")),
        "benefit_type": clean(row.get("types_of_benefits")),
        "sponsored_by": clean(row.get("sponsored_by")),
        "funding_pattern": clean(row.get("funding_pattern")),
        "how_to_avail": clean(row.get("how_to_avail")),
        "description": clean(row.get("description")),
        "source_url": clean(row.get("source_url")),
    }

    query = """
    MERGE (s:Scheme {name: $scheme_title})
    SET
        s.department = $department,
        s.beneficiaries = $beneficiaries,
        s.benefit_type = $benefit_type,
        s.sponsored_by = $sponsored_by,
        s.funding_pattern = $funding_pattern,
        s.how_to_avail = $how_to_avail,
        s.description = $description,
        s.source_url = $source_url
    """
    run_write(session, query, params)

    if params["department"]:
        query = """
        MATCH (s:Scheme {name: $scheme_title})
        MERGE (d:Department {name: $department})
        MERGE (s)-[:BELONGS_TO]->(d)
        """
        run_write(session, query, params)

    if params["beneficiaries"]:
        query = """
        MATCH (s:Scheme {name: $scheme_title})
        MERGE (b:Beneficiary {name: $beneficiaries})
        MERGE (s)-[:FOR_BENEFICIARY]->(b)
        """
        run_write(session, query, params)

    if params["benefit_type"]:
        query = """
        MATCH (s:Scheme {name: $scheme_title})
        MERGE (bt:BenefitType {name: $benefit_type})
        MERGE (s)-[:PROVIDES_BENEFIT]->(bt)
        """
        run_write(session, query, params)

    if params["sponsored_by"]:
        query = """
        MATCH (s:Scheme {name: $scheme_title})
        MERGE (sp:Sponsor {name: $sponsored_by})
        MERGE (s)-[:SPONSORED_BY]->(sp)
        """
        run_write(session, query, params)

    for keyword in get_keywords(row):
        query = """
        MATCH (s:Scheme {name: $scheme_title})
        MERGE (k:Keyword {name: $keyword})
        MERGE (s)-[:HAS_KEYWORD]->(k)
        """
        run_write(session, query, {
            "scheme_title": scheme_title,
            "keyword": keyword,
        })


def main():
    if not os.path.exists(CSV_PATH):
        print("CSV file not found.")
        print("Please run: python scrape_schemes.py")
        return

    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        print("Neo4j environment variables are missing.")
        print("Please check your .env file.")
        return

    df = pd.read_csv(CSV_PATH)

    print(f"Total scheme records found in CSV: {len(df)}")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            print("Creating Neo4j constraints...")
            create_constraints(session)

            print("Loading schemes into Neo4j Knowledge Graph...")

            for _, row in df.iterrows():
                create_scheme_graph(session, row)

            print("Knowledge Graph loaded successfully into Neo4j AuraDB.")

    except Exception as error:
        print("Failed to load graph into Neo4j.")
        print(error)

    finally:
        driver.close()


if __name__ == "__main__":
    main()