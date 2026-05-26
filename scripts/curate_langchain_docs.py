#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import hashlib
import shutil
import textwrap

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_BASE = PROJECT_ROOT / "data/raw/public/langchain/docs/src"
CURATED_BASE = PROJECT_ROOT / "data/curated/public/langchain"

DOCS_TO_CURATE = [
    {
        "src": "langsmith/evaluate-rag-tutorial.mdx",
        "category": "evaluation",
        "tags": ["langsmith", "rag", "evaluation"],
    },
    {
        "src": "langsmith/evaluation-concepts.mdx",
        "category": "evaluation",
        "tags": ["langsmith", "evaluation", "llmops"],
    },
    {
        "src": "langsmith/observability-concepts.mdx",
        "category": "observability",
        "tags": ["langsmith", "observability", "tracing"],
    },
    {
        "src": "langsmith/trace-with-langgraph.mdx",
        "category": "observability",
        "tags": ["langsmith", "langgraph", "tracing"],
    },
    {
        "src": "langsmith/prompt-engineering-concepts.mdx",
        "category": "prompt-engineering",
        "tags": ["langsmith", "prompts", "prompt-engineering"],
    },
    {
        "src": "oss/langgraph/index.mdx",
        "category": "agents-workflows",
        "tags": ["langgraph", "agents", "workflows"],
    },
]

def strip_existing_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text

def make_doc_id(rel_path: str) -> str:
    return "langchain-" + rel_path.replace("/", "-").replace(".mdx", "").replace(".md", "")

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

def yaml_list(items):
    return "\n".join(f'  - "{item}"' for item in items)

def build_frontmatter(item, body: str, target_rel_path: str) -> str:
    rel = item["src"]
    title = Path(rel).stem.replace("-", " ").title()

    return textwrap.dedent(f"""\
    ---
    doc_id: "{make_doc_id(rel)}"
    title: "{title}"
    source_type: "public"
    vendor: "langchain"
    doc_type: "vendor_documentation"
    category: "{item["category"]}"
    source_path: "public/langchain/{target_rel_path}"
    original_path: "{rel}"
    url: "https://github.com/langchain-ai/docs/blob/main/src/{rel}"
    organization: "LangChain"
    classification: "public"
    visibility: "public"
    status: "current"
    tags:
    {yaml_list(item["tags"])}
    content_hash: "{content_hash(body)}"
    metadata_added_on: "{date.today().isoformat()}"
    ---
    """).strip() + "\n\n"

def main():
    CURATED_BASE.mkdir(parents=True, exist_ok=True)

    copied = 0
    missing = []

    for item in DOCS_TO_CURATE:
        src_path = RAW_BASE / item["src"]

        if not src_path.exists():
            missing.append(str(src_path))
            continue

        body = src_path.read_text(encoding="utf-8")
        body = strip_existing_frontmatter(body)

        target_rel = item["src"]
        target_path = CURATED_BASE / target_rel
        target_path.parent.mkdir(parents=True, exist_ok=True)

        frontmatter = build_frontmatter(item, body, target_rel)
        target_path.write_text(frontmatter + body, encoding="utf-8")

        copied += 1

    print(f"Curated {copied} LangChain docs into {CURATED_BASE}")

    if missing:
        print("\nMissing files:")
        for path in missing:
            print(f" - {path}")

if __name__ == "__main__":
    main()