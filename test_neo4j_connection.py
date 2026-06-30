import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def main():
    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        print("Neo4j environment variables are missing.")
        print("Please check your .env file.")
        return

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("RETURN 'Neo4j Aura connection successful' AS message")
            record = result.single()
            print(record["message"])

    except Exception as error:
        print("Neo4j connection failed.")
        print(error)

    finally:
        driver.close()


if __name__ == "__main__":
    main()