import os
import shutil
import pandas as pd
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

CSV_PATH = "data/tn_scheme_details.csv"
DB_PATH = "vector_db"
COLLECTION_NAME = "tn_scheme_details"


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def load_documents():
    df = pd.read_csv(CSV_PATH)

    documents = []

    for _, row in df.iterrows():
        scheme_title = clean(row.get("scheme_title"))
        department = clean(row.get("concerned_department"))
        district = clean(row.get("concerned_district"))
        organisation = clean(row.get("organisation_name"))
        sponsored_by = clean(row.get("sponsored_by"))
        funding_pattern = clean(row.get("funding_pattern"))
        beneficiaries = clean(row.get("beneficiaries"))
        benefit_type = clean(row.get("types_of_benefits"))
        income = clean(row.get("income"))
        age_from = clean(row.get("age_from"))
        age_to = clean(row.get("age_to"))
        community = clean(row.get("community"))
        how_to_avail = clean(row.get("how_to_avail"))
        description = clean(row.get("description"))
        scheme_type = clean(row.get("scheme_type"))
        source_url = clean(row.get("source_url"))

        text = f"""
Scheme Title: {scheme_title}
Department: {department}
Concerned District: {district}
Organisation Name: {organisation}
Sponsored By: {sponsored_by}
Funding Pattern: {funding_pattern}
Beneficiaries: {beneficiaries}
Types of Benefits: {benefit_type}

Eligibility Criteria:
Income: {income}
Age From: {age_from}
Age To: {age_to}
Community: {community}

How To Avail:
{how_to_avail}

Description:
{description}

Scheme Type:
{scheme_type}

Official Source URL:
{source_url}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "scheme_title": scheme_title,
                    "department": department,
                    "beneficiaries": beneficiaries,
                    "benefit_type": benefit_type,
                    "source_url": source_url,
                },
            )
        )

    return documents


def main():
    if not os.path.exists(CSV_PATH):
        print("CSV file not found. Please run scrape_schemes.py first.")
        return

    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    print("Loading documents from CSV...")
    documents = load_documents()

    print(f"Total documents loaded: {len(documents)}")

    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("Creating Chroma vector database...")
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME,
    )

    print("Vector database created successfully.")
    print(f"Saved inside: {DB_PATH}")


if __name__ == "__main__":
    main()