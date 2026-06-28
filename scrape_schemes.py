import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.tn.gov.in/"
LIST_URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="
OUTPUT_FILE = "data/tn_scheme_details.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


def find_scheme_links():
    print("Opening scheme list page...")
    soup = get_soup(LIST_URL)

    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        title = a.get_text(" ", strip=True)
        href = a["href"].strip()

        if "scheme_details.php" not in href:
            continue

        full_url = urljoin(BASE_URL, href)

        if full_url in seen:
            continue

        seen.add(full_url)

        links.append({
            "scheme_title_from_list": title,
            "scheme_url": full_url
        })

    return links


def extract_label_value_data(soup: BeautifulSoup):
    data = {}

    rows = soup.find_all("tr")

    for row in rows:
        cells = row.find_all(["td", "th"])

        if len(cells) >= 2:
            key = cells[0].get_text(" ", strip=True)
            value = cells[1].get_text(" ", strip=True)

            key = key.replace(":", "").strip()
            value = value.strip()

            if key:
                data[key] = value

    return data


def get_value(data: dict, possible_keys: list):
    for key in possible_keys:
        for actual_key, value in data.items():
            if key.lower() in actual_key.lower():
                return value
    return ""


def scrape_scheme_detail(url: str):
    soup = get_soup(url)
    table_data = extract_label_value_data(soup)

    page_text = soup.get_text("\n", strip=True)

    scheme = {
        "source_url": url,
        "concerned_department": get_value(table_data, ["Concerned Department"]),
        "concerned_district": get_value(table_data, ["Concerned District"]),
        "organisation_name": get_value(table_data, ["Organisation Name"]),
        "scheme_title": get_value(table_data, ["Scheme Title", "Scheme Title/Name"]),
        "associated_scheme": get_value(table_data, ["Associated Scheme"]),
        "sponsored_by": get_value(table_data, ["Sponsered By", "Sponsored By"]),
        "funding_pattern": get_value(table_data, ["Funding Pattern"]),
        "beneficiaries": get_value(table_data, ["Beneficiaries"]),
        "types_of_benefits": get_value(table_data, ["Types of Benefits"]),
        "income": get_value(table_data, ["Income"]),
        "age_from": get_value(table_data, ["Age From"]),
        "age_to": get_value(table_data, ["Age To"]),
        "community": get_value(table_data, ["Community"]),
        "how_to_avail": get_value(table_data, ["How To avail", "How To Avail"]),
        "introduced_on": get_value(table_data, ["Introduced On"]),
        "description": get_value(table_data, ["Description"]),
        "scheme_type": get_value(table_data, ["Scheme Type"]),
        "raw_text": page_text
    }

    return scheme


def main():
    os.makedirs("data", exist_ok=True)

    scheme_links = find_scheme_links()

    print(f"Total scheme links found: {len(scheme_links)}")

    if not scheme_links:
        print("No scheme links found. Please check the page structure or internet connection.")
        return

    all_schemes = []

    for index, item in enumerate(scheme_links, start=1):
        print(f"{index}. Scraping: {item['scheme_title_from_list']}")

        try:
            details = scrape_scheme_detail(item["scheme_url"])

            if not details["scheme_title"]:
                details["scheme_title"] = item["scheme_title_from_list"]

            all_schemes.append(details)
            time.sleep(1)

        except Exception as error:
            print(f"Failed to scrape: {item['scheme_url']}")
            print(error)

    df = pd.DataFrame(all_schemes)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("Scraping completed.")
    print(f"Saved file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()