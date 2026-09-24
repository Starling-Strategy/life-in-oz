#!/usr/bin/env python3
"""Validate the released dataset offline, using only Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate(root=ROOT):
    root = Path(root)
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def local_file(relative):
        path = root / relative
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Path escapes the dataset: " + relative)
        return path

    manifest = load(root / "manifest.json")
    documents = manifest["documents"]
    ids = [d["id"] for d in documents]
    check(len(ids) == len(set(ids)), "Duplicate document IDs")
    check(manifest["synthetic"] is True, "Missing fictional classification")
    check(manifest["real_events_or_recordings"] is False, "Real-recording flag")
    check(manifest["license"] == "CC0-1.0", "Unexpected license")
    check(manifest["total_documents"] == len(documents), "Document total mismatch")
    people = load(root / "world/people.json")["members"]
    person_ids = {p["id"] for p in people}
    check(len(person_ids) == len(people), "Duplicate person IDs")
    for person in people:
        for friend in person["relationships"]:
            check(friend in person_ids, "Unknown relationship: " + friend)
    reference_members = load(root / "evaluation/members.json")["members"]
    check({p["id"] for p in reference_members} == person_ids, "Reference member IDs mismatch")

    blocks = {}
    members_by_source = {}
    words = 0
    paired_paths = set()
    for doc in documents:
        label = doc["id"]
        text_path = local_file(doc["text_file"])
        json_path = local_file(doc["canonical_blocks_file"])
        paired_paths.update((doc["text_file"], doc["canonical_blocks_file"]))
        text_bytes = text_path.read_bytes()
        source = load(json_path)
        check(digest(text_bytes) == doc["text_sha256"], "Text hash mismatch: " + label)
        check(b"SYNTHETIC SOURCE" in text_bytes, "Missing fiction banner: " + label)
        check(source["fictional"] is True, "Missing source fiction flag: " + label)
        check(source["id"] == label, "Source ID mismatch: " + label)
        check(source["title"] == doc["title"], "Source title mismatch: " + label)
        check(source["format"] == doc["format"], "Source format mismatch: " + label)
        check(source["members"] == doc["member_ids"], "Member list mismatch: " + label)
        check(set(source["members"]) <= person_ids, "Unknown source member: " + label)
        canonical = json.dumps(source["blocks"], ensure_ascii=False).encode("utf-8")
        check(digest(canonical) == doc["content_sha256"] == source["content_sha256"],
              "Block hash mismatch: " + label)
        block_ids = [b["id"] for b in source["blocks"]]
        check(len(block_ids) == len(set(block_ids)), "Duplicate block IDs: " + label)
        for block in source["blocks"]:
            normalized = "\n".join(line.rstrip() for line in block["text"].splitlines())
            check(normalized in text_bytes.decode("utf-8"), "Block missing from text: " + label)
        blocks[label] = {b["id"]: b["text"] for b in source["blocks"]}
        members_by_source[label] = set(source["members"])
        count = sum(len(b["text"].split()) for b in source["blocks"])
        words += count
        check(count == doc["words"], "Word count mismatch: " + label)
    actual_paths = {p.relative_to(root).as_posix() for p in (root / "sources").iterdir() if p.is_file()}
    check(actual_paths == paired_paths, "Unregistered or missing source files")
    check(len(paired_paths) == len(documents) * 2, "Source paths reused")
    check(words == manifest["total_words"], "Word total mismatch")

    collection_membership = {}
    for path in sorted((root / "collections").glob("*.json")):
        collection = load(path)
        cid = collection["id"]
        wanted = {d["id"] for d in documents if d["collection_id"] == cid}
        selected = collection["document_ids"]
        check(len(selected) == len(set(selected)), "Duplicate collection entry: " + cid)
        check(set(selected) == wanted, "Collection membership mismatch: " + cid)
        check(collection["total_documents"] == len(selected), "Collection total mismatch: " + cid)
        check(collection["total_words"] == sum(d["words"] for d in documents if d["id"] in wanted),
              "Collection words mismatch: " + cid)
        for source_id in selected:
            check(source_id not in collection_membership, "Overlapping collection: " + source_id)
            collection_membership[source_id] = cid
    check(set(collection_membership) == set(ids), "Missing collection assignment")

    evaluation = load(root / "evaluation/experience-leads.json")
    check(evaluation["collection_id"] == "community-life", "Unexpected annotation scope")
    check(evaluation["human_verification"] is False, "Unexpected human-verification claim")
    leads = evaluation["experience_leads"]
    check(len(leads) == evaluation["total_leads"], "Lead total mismatch")
    episode_keys = [(lead["person_id"], lead["episode_key"]) for lead in leads]
    check(len(episode_keys) == len(set(episode_keys)), "Duplicate reference episode")
    anchors = 0
    for lead in leads:
        check(lead["person_id"] in person_ids, "Unknown lead person")
        check(bool(lead["evidence"]), "Lead without evidence")
        for anchor in lead["evidence"]:
            anchors += 1
            sid, bid = anchor["source_id"], anchor["block_id"]
            check(collection_membership.get(sid) == evaluation["collection_id"], "Annotation crosses collection: " + sid)
            if sid not in blocks or bid not in blocks[sid]:
                errors.append("Missing evidence block: " + sid + "/" + bid)
                continue
            text = blocks[sid][bid]
            start, end = anchor["start"], anchor["end"]
            check(type(start) is int and type(end) is int and 0 <= start < end <= len(text),
                  "Invalid evidence bounds: " + sid + "/" + bid)
            check(text == anchor["context"], "Evidence context mismatch: " + sid + "/" + bid)
            check(text[start:end] == anchor["quote"], "Evidence quote mismatch: " + sid + "/" + bid)
            check(lead["person_id"] in members_by_source[sid], "Evidence person mismatch: " + sid)
    for row in evaluation["member_coverage"]:
        pid = row["person_id"]
        check(row["experience_leads"] == sum(lead["person_id"] == pid for lead in leads),
              "Person lead total mismatch: " + pid)
        evidence_sources = {anchor["source_id"] for lead in leads if lead["person_id"] == pid
                            for anchor in lead["evidence"]}
        check(row["source_documents"] == len(evidence_sources), "Person evidence source total mismatch: " + pid)

    origin = load(root / "provenance/source-hashes.json")["sources"]
    check(len(origin) == len(documents), "Origin source total mismatch")
    check({x["id"]: (x["text_sha256"], x["content_sha256"]) for x in origin} ==
          {x["id"]: (x["text_sha256"], x["content_sha256"]) for x in documents},
          "Preserved source hashes changed")
    if errors:
        raise ValueError("\n".join(errors))
    return {"documents": len(documents), "roster_members": len(people), "words": words,
            "reference_experiences": len(leads), "evidence_anchors": anchors,
            "collections": sorted(set(collection_membership.values()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = validate(args.root)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, "Validation failed: " + str(exc) + "\n")
    print(json.dumps({"status": "passed", **result}, indent=2))


if __name__ == "__main__":
    main()
