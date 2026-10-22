#!/usr/bin/env python3
"""Validate the released dataset offline, using only Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {
    "news_article", "email_thread", "email_exchange", "social_thread", "webinar", "conversation_transcript",
    "magazine_feature", "manager_conversation", "newsletter_feature", "intake_email", "panel_transcript",
    "post_event_debrief", "nomination_letter", "meeting_minutes", "press_release", "survey_response",
    "radio_interview", "speaker_bio", "grant_report", "membership_intake_form",
}
# Collection -> (roster, reference identities, reference annotations). Collections not listed have no roster.
ROSTERS = {
    "community-life": ("world/people.json", "evaluation/members.json", "evaluation/experience-leads.json"),
    "book-adventures": ("world/people.json", None, None),
    "leadership-network": ("world/leadership-network-people.json", "evaluation/leadership-network-members.json",
                           "evaluation/leadership-network-experience-leads.json"),
}
QUERY_FILES = {"leadership-network": "evaluation/leadership-network-queries.json"}
QUERY_KINDS = {"vocabulary-gap", "exact-term", "skill/sector/place", "speaker/convening", "negative-no-answer"}


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
    roster_ids = {}
    roster_sizes = {}
    for cid, (roster_path, reference_path, _) in ROSTERS.items():
        if roster_path in roster_ids or not (root / roster_path).exists():
            continue
        people = load(root / roster_path)["members"]
        ids_here = {p["id"] for p in people}
        check(len(ids_here) == len(people), "Duplicate person IDs: " + roster_path)
        names = [(p["first_name"], p["last_name"]) for p in people]
        check(len(names) == len(set(names)), "Duplicate full names: " + roster_path)
        for person in people:
            for friend in person["relationships"]:
                check(friend in ids_here, "Unknown relationship: " + friend)
        roster_ids[roster_path] = ids_here
        roster_sizes[roster_path] = len(people)
    for cid, (roster_path, reference_path, _) in ROSTERS.items():
        if reference_path and roster_path in roster_ids:
            reference_members = load(root / reference_path)["members"]
            check({p["id"] for p in reference_members} == roster_ids[roster_path],
                  "Reference member IDs mismatch: " + reference_path)
    person_ids = roster_ids["world/people.json"]

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
        check(doc["format"] in FORMATS, "Unknown format label: " + label)
        check(doc["collection_id"] in ROSTERS, "Unknown collection: " + label)
        roster = roster_ids.get(ROSTERS.get(doc["collection_id"], ("",))[0], set())
        check(set(source["members"]) <= roster, "Unknown source member: " + label)
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

    leads_total = anchors = 0
    per_collection = {}
    lead_keys = {}
    for cid, (roster_path, _, annotation_path) in sorted(ROSTERS.items()):
        if not annotation_path or not (root / annotation_path).exists():
            continue
        roster = roster_ids[roster_path]
        evaluation = load(root / annotation_path)
        check(evaluation["collection_id"] == cid, "Unexpected annotation scope: " + annotation_path)
        check(evaluation["human_verification"] is False, "Unexpected human-verification claim")
        leads = evaluation["experience_leads"]
        check(len(leads) == evaluation["total_leads"], "Lead total mismatch")
        episode_keys = [(lead["person_id"], lead["episode_key"]) for lead in leads]
        check(len(episode_keys) == len(set(episode_keys)), "Duplicate reference episode")
        lead_keys[cid] = set(episode_keys)
        collection_anchors = 0
        for lead in leads:
            check(lead["person_id"] in roster, "Unknown lead person")
            check(bool(lead["evidence"]), "Lead without evidence")
            for anchor in lead["evidence"]:
                collection_anchors += 1
                sid, bid = anchor["source_id"], anchor["block_id"]
                check(collection_membership.get(sid) == cid, "Annotation crosses collection: " + sid)
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
        leads_total += len(leads)
        anchors += collection_anchors
        per_collection[cid] = {"reference_experiences": len(leads), "evidence_anchors": collection_anchors}

    queries_total = 0
    for cid, query_path in QUERY_FILES.items():
        if not (root / query_path).exists():
            continue
        roster = roster_ids[ROSTERS[cid][0]]
        query_file = load(root / query_path)
        check(query_file["collection_id"] == cid, "Unexpected query scope: " + query_path)
        query_ids = [q["id"] for q in query_file["queries"]]
        check(len(query_ids) == len(set(query_ids)), "Duplicate query IDs")
        for q in query_file["queries"]:
            check(q["kind"] in QUERY_KINDS, "Unknown query kind: " + q["id"])
            expected = q["expected_member_ids"]
            check(set(expected) <= roster, "Unknown expected member: " + q["id"])
            check((q["kind"] == "negative-no-answer") == (not expected), "Negative query mismatch: " + q["id"])
            check(set(q["support"]) == set(expected), "Query support mismatch: " + q["id"])
            for pid, support in q["support"].items():
                check(bool(support["source_ids"]), "Unsupported expected member: " + q["id"] + "/" + pid)
                for sid in support["source_ids"]:
                    check(collection_membership.get(sid) == cid, "Query source outside collection: " + q["id"])
                    check(pid in members_by_source.get(sid, set()), "Query source lacks member: " + q["id"])
                has_lead = any((pid, key) in lead_keys.get(cid, set()) for key in support["episode_keys"])
                check(support["reference_lead"] == has_lead, "Query lead flag mismatch: " + q["id"])
        queries_total += len(query_ids)

    origin = load(root / "provenance/source-hashes.json")["sources"]
    check(len(origin) == len(documents), "Origin source total mismatch")
    check({x["id"]: (x["text_sha256"], x["content_sha256"]) for x in origin} ==
          {x["id"]: (x["text_sha256"], x["content_sha256"]) for x in documents},
          "Preserved source hashes changed")
    if errors:
        raise ValueError("\n".join(errors))
    return {"documents": len(documents), "roster_members": sum(roster_sizes.values()), "words": words,
            "reference_experiences": leads_total, "evidence_anchors": anchors, "queries": queries_total,
            "collections": sorted(set(collection_membership.values())),
            "by_collection": {cid: dict(per_collection.get(cid, {}),
                                        documents=sum(1 for d in documents if d["collection_id"] == cid),
                                        words=sum(d["words"] for d in documents if d["collection_id"] == cid))
                              for cid in sorted(set(collection_membership.values()))}}


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
