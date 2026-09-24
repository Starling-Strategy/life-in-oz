#!/usr/bin/env python3
"""List text paths for one collection, without printing hidden annotations."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def select(collection_id, root=ROOT):
    collections = {p.stem: p for p in (root / "collections").glob("*.json")}
    if collection_id not in collections:
        raise ValueError("Unknown collection: " + collection_id)
    collection = json.loads(collections[collection_id].read_text(encoding="utf-8"))
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    by_id = {doc["id"]: doc["text_file"] for doc in manifest["documents"]}
    return [by_id[source_id] for source_id in collection["document_ids"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", choices=["community-life", "book-adventures"])
    args = parser.parse_args()
    for path in select(args.collection):
        print(path)


if __name__ == "__main__":
    main()
