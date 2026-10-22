"""The real package must pass; corrupted copies must fail."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


validator = module("validate")
selector = module("select")


class DatasetTests(unittest.TestCase):
    def test_release(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["documents"], 576)
        self.assertEqual(result["roster_members"], 350)
        self.assertEqual(result["evidence_anchors"], 2006)
        self.assertEqual(result["reference_experiences"], 1379)
        self.assertEqual(result["queries"], 62)
        self.assertEqual(result["by_collection"]["community-life"]["reference_experiences"], 156)
        self.assertEqual(result["by_collection"]["community-life"]["evidence_anchors"], 326)
        network = result["by_collection"]["leadership-network"]
        self.assertEqual(network["documents"], 523)
        self.assertEqual(network["reference_experiences"], 1223)
        self.assertEqual(network["evidence_anchors"], 1680)

    def test_leadership_network_coverage(self):
        leads = json.loads((ROOT / "evaluation/leadership-network-experience-leads.json").read_text(encoding="utf-8"))
        counts = [row["experience_leads"] for row in leads["member_coverage"]]
        self.assertEqual(len(counts), 300)
        self.assertTrue(all(3 <= n <= 5 for n in counts))
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        docs = [d for d in manifest["documents"] if d["collection_id"] == "leadership-network"]
        self.assertGreaterEqual(sum(len(d["member_ids"]) > 1 for d in docs) / len(docs), 0.7)
        self.assertEqual(len({d["format"] for d in docs}), 17)

    def test_selection(self):
        modern = selector.select("community-life")
        fantasy = selector.select("book-adventures")
        network = selector.select("leadership-network")
        self.assertEqual(len(modern), 48)
        self.assertEqual(len(fantasy), 5)
        self.assertEqual(len(network), 523)
        self.assertFalse(set(modern) & set(fantasy) or set(modern) & set(network) or set(fantasy) & set(network))
        self.assertTrue(all(p.startswith("sources/") and p.endswith(".txt") for p in modern + fantasy + network))
        with self.assertRaises(ValueError):
            selector.select("../world/people")

    def corrupted(self, relative, change, expected):
        with tempfile.TemporaryDirectory(prefix="life-in-oz-test-") as folder:
            target = Path(folder)
            for name in ["sources", "world", "collections", "evaluation", "provenance"]:
                shutil.copytree(ROOT / name, target / name)
            shutil.copy2(ROOT / "manifest.json", target / "manifest.json")
            path = target / relative
            if path.suffix == ".json":
                value = json.loads(path.read_text(encoding="utf-8"))
                change(value)
                path.write_text(json.dumps(value), encoding="utf-8")
            else:
                path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, expected):
                validator.validate(target)

    def test_changed_text_fails(self):
        self.corrupted("sources/oz-01-civic-news.txt", lambda text: text + "Changed.\n", "Text hash mismatch")

    def test_changed_blocks_fail(self):
        self.corrupted("sources/oz-01-civic-news.json",
                       lambda v: v["blocks"][0].update(text="Invented replacement"), "Block hash mismatch")

    def test_wrong_evidence_fails(self):
        self.corrupted("evaluation/experience-leads.json",
                       lambda v: v["experience_leads"][0]["evidence"][0].update(quote="Unsupported quote"),
                       "Evidence quote mismatch")

    def test_wrong_scope_fails(self):
        self.corrupted("evaluation/experience-leads.json",
                       lambda v: v["experience_leads"][0]["evidence"][0].update(source_id="oz-14-woodman-trail-clearing"),
                       "Annotation crosses collection")

    def test_wrong_collection_fails(self):
        self.corrupted("collections/community-life.json", lambda v: v["document_ids"].pop(),
                       "Collection membership mismatch")

    def test_wrong_total_fails(self):
        self.corrupted("manifest.json", lambda v: v.update(total_words=0), "Word total mismatch")

    def test_unknown_person_fails(self):
        self.corrupted("world/people.json", lambda v: v["members"][0]["relationships"].append("missing"),
                       "Unknown relationship")

    def test_network_evidence_fails(self):
        self.corrupted("evaluation/leadership-network-experience-leads.json",
                       lambda v: v["experience_leads"][0]["evidence"][0].update(quote="Unsupported quote"),
                       "Evidence quote mismatch")

    def test_network_scope_fails(self):
        self.corrupted("evaluation/leadership-network-experience-leads.json",
                       lambda v: v["experience_leads"][0]["evidence"][0].update(source_id="oz-01-civic-news"),
                       "Annotation crosses collection")

    def test_network_member_fails(self):
        self.corrupted("sources/ln-001-survey-response.json", lambda v: v["members"].append("m001"),
                       "Member list mismatch")

    def test_unknown_format_fails(self):
        def change(v):
            doc = next(d for d in v["documents"] if d["collection_id"] == "leadership-network")
            doc["format"] = "carrier_pigeon"
        self.corrupted("manifest.json", change, "Unknown format label")

    def test_duplicate_full_name_fails(self):
        def change(v):
            v["members"][1]["first_name"] = v["members"][0]["first_name"]
            v["members"][1]["last_name"] = v["members"][0]["last_name"]
        self.corrupted("world/leadership-network-people.json", change, "Duplicate full names")

    def test_unsupported_query_fails(self):
        self.corrupted("evaluation/leadership-network-queries.json",
                       lambda v: v["queries"][0]["support"]["ln001"].update(source_ids=[]),
                       "Unsupported expected member")

    def test_query_member_outside_source_fails(self):
        self.corrupted("evaluation/leadership-network-queries.json",
                       lambda v: v["queries"][0]["support"]["ln001"].update(source_ids=["ln-001-survey-response"]),
                       "Query source lacks member")

    def test_negative_query_with_answer_fails(self):
        def change(v):
            q = next(q for q in v["queries"] if q["kind"] == "negative-no-answer")
            q["expected_member_ids"] = ["ln001"]
        self.corrupted("evaluation/leadership-network-queries.json", change, "Negative query mismatch")

    def test_path_escape_fails(self):
        self.corrupted("manifest.json", lambda v: v["documents"][0].update(text_file="../outside.txt"),
                       "Path escapes")


if __name__ == "__main__":
    unittest.main()
