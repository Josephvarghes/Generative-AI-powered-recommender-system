import requests
from bs4 import BeautifulSoup
import json
import os
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

BASE_URL = "https://www.shl.com"

TOOLTIP_MAP = {
    "A": "Ability and Aptitude",
    "B": "Biodata and Situational Judgment",
    "C": "Competency",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge and Skill",
    "P": "Personality and Behavioral",
    "S": "Situation"
}

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_details_from_page(url):
    try:
        soup = get_html(url)
        duration = None
        remote_testing = "No"
        adaptive_support = "No"

        for p in soup.find_all("p"):
            text = p.get_text().lower()
            if "minutes" in text or "duration" in text:
                duration = text.strip()
            if "remote" in text:
                remote_testing = "Yes"
            if "adaptive" in text or "irt" in text:
                adaptive_support = "Yes"

        return duration, remote_testing, adaptive_support
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, "No", "No"

def get_prepackaged_job_roles(soup):
    job_roles = []

    th = soup.find("th", string="Pre-packaged Job Solutions")
    if not th:
        print("Section not found.")
        return job_roles

    table = th.find_parent("table")
    if not table:
        print("Table not found.")
        return job_roles

    for tr in table.find_all("tr"):
        td_title = tr.find("td", class_="custom__table-heading__title")
        type_td = tr.find("td", class_="product-catalogue__keys")

        if td_title:
            a_tag = td_title.find("a")
            if a_tag and a_tag.get("href"):
                name = a_tag.get_text(strip=True)
                link = BASE_URL + a_tag["href"]

                test_types = []
                if type_td:
                    spans = type_td.find_all("span", class_="product-catalogue__key")
                    test_types = [TOOLTIP_MAP.get(span.text.strip(), span.text.strip()) for span in spans]

                job_roles.append({
                    "name": name,
                    "url": link,
                    "test_types": test_types
                })

    return job_roles

def save_data_to_json(new_data, path="data/assessments.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    combined_data = existing_data + new_data

    # Remove duplicates by name
    seen = set()
    unique_data = []
    for item in combined_data:
        if item["name"] not in seen:
            unique_data.append(item)
            seen.add(item["name"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(unique_data, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(unique_data)} assessments saved to {path}")

def scrape_all_jobs(catalog_url):
    print("🔍 Scraping all job roles from SHL...")
    soup = get_html(catalog_url)
    job_roles = get_prepackaged_job_roles(soup)

    all_results = []

    for i, job in enumerate(job_roles):
        print(f"[{i+1}/{len(job_roles)}] Fetching: {job['name']}")
        duration, remote, adaptive = get_details_from_page(job["url"])
        time.sleep(1)

        result = {
            "name": job["name"],
            "url": job["url"],
            "duration": duration,
            "remote_testing": remote,
            "adaptive_support": adaptive,
            "test_types": job.get("test_types", [])
        }
        all_results.append(result)

    save_data_to_json(all_results)

if __name__ == "__main__":
    catalog_url = "https://www.shl.com/solutions/products/product-catalog/"
    scrape_all_jobs(catalog_url)
