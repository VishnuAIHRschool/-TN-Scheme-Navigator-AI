import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def main():
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )

    query = """
    MATCH (s:Scheme)-[:SPONSORED_BY]->(sp:Sponsor)
    WHERE toLower(sp.name) CONTAINS "state"
    RETURN s.name AS scheme, sp.name AS sponsored_by
    LIMIT 25
    """

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query)

            print("Schemes sponsored by State:")
            print("---------------------------")

            for record in result:
                print(f"- {record['scheme']} | Sponsored By: {record['sponsored_by']}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()