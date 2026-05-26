#!/usr/bin/env python3

from pathlib import Path
from datetime import date
import hashlib
import textwrap
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURATED_BASE = PROJECT_ROOT / "data/curated/public/qdrant"

QDRANT_DOCS = [
    {
        "url": "https://qdrant.tech/documentation/manage-data/index.md",
        "target": "manage-data/overview.md",
        "title": "Qdrant Manage Data Overview",
        "category": "manage-data",
        "tags": ["qdrant", "manage-data"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/points/index.md",
        "target": "manage-data/points.md",
        "title": "Qdrant Points",
        "category": "manage-data",
        "tags": ["qdrant", "points", "vectors"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/vectors/index.md",
        "target": "manage-data/vectors.md",
        "title": "Qdrant Vectors",
        "category": "manage-data",
        "tags": ["qdrant", "vectors", "embeddings"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/payload/index.md",
        "target": "manage-data/payload.md",
        "title": "Qdrant Payload",
        "category": "manage-data",
        "tags": ["qdrant", "payload", "metadata"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/collections/index.md",
        "target": "manage-data/collections.md",
        "title": "Qdrant Collections",
        "category": "manage-data",
        "tags": ["qdrant", "collections"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/indexing/index.md",
        "target": "manage-data/indexing.md",
        "title": "Qdrant Indexing",
        "category": "manage-data",
        "tags": ["qdrant", "indexing", "performance"],
    },
    {
        "url": "https://qdrant.tech/documentation/manage-data/multitenancy/index.md",
        "target": "manage-data/multitenancy.md",
        "title": "Qdrant Multitenancy",
        "category": "manage-data",
        "tags": ["qdrant", "multitenancy", "tenant-isolation"],
    },
    {
        "url": "https://qdrant.tech/documentation/search/search/index.md",
        "target": "search/search.md",
        "title": "Qdrant Search",
        "category": "search",
        "tags": ["qdrant", "search", "similarity-search"],
    },
    {
        "url": "https://qdrant.tech/documentation/search/filtering/index.md",
        "target": "search/filtering.md",
        "title": "Qdrant Filtering",
        "category": "search",
        "tags": ["qdrant", "filtering", "payload"],
    },
    {
        "url": "https://qdrant.tech/documentation/search/hybrid-queries/index.md",
        "target": "search/hybrid-queries.md",
        "title": "Qdrant Hybrid Queries",
        "category": "search",
        "tags": ["qdrant", "hybrid-search", "rag"],
    },
    {
        "url": "https://qdrant.tech/documentation/search/search-relevance/index.md",
        "target": "search/search-relevance.md",
        "title": "Qdrant Search Relevance",
        "category": "search",
        "tags": ["qdrant", "search-relevance", "ranking"],
    },
    {
        "url": "https://qdrant.tech/documentation/search/low-latency-search/index.md",
        "target": "search/low-latency-search.md",
        "title": "Qdrant Low Latency Search",
        "category": "search",
        "tags": ["qdrant", "latency", "performance"],
    },
    {
        "url": "https://qdrant.tech/documentation/inference/index.md",
        "target": "inference/inference.md",
        "title": "Qdrant Inference",
        "category": "inference",
        "tags": ["qdrant", "inference", "embeddings"],
    },
]


def strip_existing_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def make_doc_id(target: str) -> str:
    return "qdrant-" + target.replace("/", "-").replace(".md", "")


def yaml_list(items: list[str]) -> str:
    return "\n".join(f'  - "{item}"' for item in items)


def build_frontmatter(item: dict, body: str) -> str:
    return textwrap.dedent(f"""\
    ---
    doc_id: "{make_doc_id(item["target"])}"
    title: "{item["title"]}"
    source_type: "public"
    vendor: "qdrant"
    doc_type: "vendor_documentation"
    category: "{item["category"]}"
    source_path: "public/qdrant/{item["target"]}"
    original_url: "{item["url"]}"
    organization: "Qdrant"
    classification: "public"
    visibility: "public"
    status: "current"
    tags:
    {yaml_list(item["tags"])}
    content_hash: "{content_hash(body)}"
    metadata_added_on: "{date.today().isoformat()}"
    ---
    """).strip() + "\n\n"


def fetch_markdown(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def main() -> None:
    CURATED_BASE.mkdir(parents=True, exist_ok=True)

    written = 0

    for item in QDRANT_DOCS:
        print(f"Fetching {item['url']}")

        body = fetch_markdown(item["url"])
        body = strip_existing_frontmatter(body)

        target_path = CURATED_BASE / item["target"]
        target_path.parent.mkdir(parents=True, exist_ok=True)

        content = build_frontmatter(item, body) + body
        target_path.write_text(content, encoding="utf-8")

        written += 1

    print(f"\nCurated {written} Qdrant docs into {CURATED_BASE}")


if __name__ == "__main__":
    main()