"""
Data.gov Catalog Ingestor
Fetches dataset metadata from catalog.data.gov and injects it into the
R3AELERPrompts.KNOWLEDGE_BASE for quick search via the Knowledge API.

Uses CKAN package_search API:
  https://catalog.data.gov/api/3/action/package_search?rows=100&start=0

Notes:
- This is a lightweight metadata ingestor (title, notes/description, URL, tags)
- Idempotent: regenerates topics using stable keys based on dataset name
- Safe defaults: short timeouts, capped rows, graceful failures
"""
from typing import List, Dict, Tuple
import requests
import logging


CKAN_SEARCH_URL = "https://catalog.data.gov/api/3/action/package_search"


def fetch_data_gov_datasets(rows: int = 100, start: int = 0, timeout: float = 8.0) -> List[Dict]:
    """Fetch dataset entries from data.gov CKAN API.

    Returns a list of dataset dicts (subset of CKAN fields).
    """
    try:
        params = {"rows": max(1, min(rows, 500)), "start": max(0, start)}
        resp = requests.get(CKAN_SEARCH_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            logging.warning("data.gov CKAN API returned success=false")
            return []
        results = data.get("result", {}).get("results", [])
        return results
    except Exception as e:
        logging.error(f"Failed to fetch data.gov catalog: {e}")
        return []


def dataset_to_kb_entry(ds: Dict) -> Tuple[str, str]:
    """Convert a CKAN dataset record into a (topic, content) pair for KB.

    Topic format: "data.gov:{name}" (lowercase, URL-safe name)
    Content: A concise block with title, description, tags, and URL
    """
    name = (ds.get("name") or "unknown").strip().lower()
    title = (ds.get("title") or name).strip()
    notes = (ds.get("notes") or "").strip()
    tags = [t.get("display_name") or t.get("name") for t in (ds.get("tags") or [])]
    # Construct dataset page URL on catalog site when possible
    url = f"https://catalog.data.gov/dataset/{name}" if name else (ds.get("url") or "")

    # Build a compact knowledge entry
    lines = [
        f"Data.gov Dataset: {title}",
        f"URL: {url}",
    ]
    if notes:
        lines.append(f"Description: {notes}")
    if tags:
        lines.append("Tags: " + ", ".join([t for t in tags if t]))

    content = "\n".join(lines)
    topic = f"data.gov:{name}" if name else f"data.gov:{title.lower()}"
    return topic, content


def ingest_into_knowledge_base(kb: Dict[str, str], rows: int = 100) -> int:
    """Fetch datasets and inject as topics into provided knowledge base dict.

    Returns the number of topics written/updated.
    """
    datasets = fetch_data_gov_datasets(rows=rows)
    if not datasets:
        return 0

    count = 0
    for ds in datasets:
        try:
            topic, content = dataset_to_kb_entry(ds)
            # Idempotent write/update
            kb[topic] = content
            count += 1
        except Exception as e:
            logging.warning(f"Skipping dataset due to parse error: {e}")

    logging.info(f"Ingested {count} data.gov datasets into KB")
    return count
