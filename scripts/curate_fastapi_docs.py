#!/usr/bin/env python3

from datetime import date

from scripts.helpers import strip_existing_frontmatter, content_hash, frontmatter_from_metadata
from app.core.config import BASE_DIR


RAW_BASE = BASE_DIR / "data/raw/public/fastapi/docs/en/docs"
CURATED_BASE = BASE_DIR / "data/curated/public/fastapi"

FASTAPI_DOCS = [
    {
        "src": "async.md",
        "target": "concepts/async.md",
        "title": "FastAPI Async",
        "category": "concepts",
        "tags": ["fastapi", "async", "concurrency"],
    },
    {
        "src": "deployment/concepts.md",
        "target": "deployment/concepts.md",
        "title": "FastAPI Deployment Concepts",
        "category": "deployment",
        "tags": ["fastapi", "deployment", "production"],
    },
    {
        "src": "deployment/docker.md",
        "target": "deployment/docker.md",
        "title": "FastAPI Docker Deployment",
        "category": "deployment",
        "tags": ["fastapi", "docker", "deployment"],
    },
    {
        "src": "deployment/server-workers.md",
        "target": "deployment/server-workers.md",
        "title": "FastAPI Server Workers",
        "category": "deployment",
        "tags": ["fastapi", "workers", "scaling"],
    },
    {
        "src": "deployment/https.md",
        "target": "deployment/https.md",
        "title": "FastAPI HTTPS",
        "category": "deployment",
        "tags": ["fastapi", "https", "security"],
    },
    {
        "src": "advanced/middleware.md",
        "target": "advanced/middleware.md",
        "title": "FastAPI Middleware",
        "category": "advanced",
        "tags": ["fastapi", "middleware", "observability"],
    },
    {
        "src": "advanced/settings.md",
        "target": "advanced/settings.md",
        "title": "FastAPI Settings",
        "category": "advanced",
        "tags": ["fastapi", "settings", "configuration"],
    },
    {
        "src": "advanced/behind-a-proxy.md",
        "target": "advanced/behind-a-proxy.md",
        "title": "FastAPI Behind a Proxy",
        "category": "advanced",
        "tags": ["fastapi", "proxy", "deployment"],
    },
    {
        "src": "advanced/events.md",
        "target": "advanced/events.md",
        "title": "FastAPI Events",
        "category": "advanced",
        "tags": ["fastapi", "events", "lifespan"],
    },
    {
        "src": "advanced/testing-dependencies.md",
        "target": "advanced/testing-dependencies.md",
        "title": "FastAPI Testing Dependencies",
        "category": "testing",
        "tags": ["fastapi", "testing", "dependencies"],
    },
    {
        "src": "how-to/testing-database.md",
        "target": "testing/testing-database.md",
        "title": "FastAPI Testing Database",
        "category": "testing",
        "tags": ["fastapi", "testing", "database"],
    },
    {
        "src": "tutorial/security/index.md",
        "target": "security/security-overview.md",
        "title": "FastAPI Security Overview",
        "category": "security",
        "tags": ["fastapi", "security", "authentication"],
    },
    {
        "src": "tutorial/security/oauth2-jwt.md",
        "target": "security/oauth2-jwt.md",
        "title": "FastAPI OAuth2 JWT",
        "category": "security",
        "tags": ["fastapi", "oauth2", "jwt", "security"],
    },
]


def make_doc_id(target: str) -> str:
    return "fastapi-" + target.replace("/", "-").replace(".md", "")


def build_frontmatter(item: dict, body: str) -> str:
    metadata = {
        "doc_id": make_doc_id(item["target"]),
        "title": item["title"],
        "source_type": "public",
        "vendor": "fastapi",
        "doc_type": "vendor_documentation",
        "category": item["category"],
        "source_path": f'public/fastapi/{item["target"]}',
        "original_path": item["src"],
        "url": f'https://github.com/fastapi/fastapi/blob/master/docs/en/docs/{item["src"]}',
        "organization": "FastAPI",
        "classification": "public",
        "visibility": "public",
        "status": "current",
        "tags": item["tags"],
        "content_hash": content_hash(body),
        "metadata_added_on": date.today().isoformat(),
    }
    return frontmatter_from_metadata(metadata)


def main() -> None:
    CURATED_BASE.mkdir(parents=True, exist_ok=True)

    written = 0
    missing = []

    for item in FASTAPI_DOCS:
        src_path = RAW_BASE / item["src"]

        if not src_path.exists():
            missing.append(str(src_path))
            continue

        body = src_path.read_text(encoding="utf-8")
        body = strip_existing_frontmatter(body)

        target_path = CURATED_BASE / item["target"]
        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_text(build_frontmatter(item, body) + body, encoding="utf-8")
        written += 1

    print(f"Curated {written} FastAPI docs into {CURATED_BASE}")

    if missing:
        print("\nMissing files:")
        for path in missing:
            print(f" - {path}")


if __name__ == "__main__":
    main()
    