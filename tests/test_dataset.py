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
        self.assertEqual(result["documents"], 53)
        self.assertEqual(result["roster_members"], 50)
        self.assertEqual(result["evidence_anchors"], 326)
        self.assertEqual(result["reference_experiences"], 156)

    def test_selection(self):
        modern = selector.select("community-life")
        fantasy = selector.select("book-adventures")
        self.assertEqual(len(modern), 48)
        self.assertEqual(len(fantasy), 5)
        self.assertFalse(set(modern) & set(fantasy))
        self.assertTrue(all(p.startswith("sources/") and p.endswith(".txt") for p in modern + fantasy))
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

    def test_path_escape_fails(self):
        self.corrupted("manifest.json", lambda v: v["documents"][0].update(text_file="../outside.txt"),
                       "Path escapes")


if __name__ == "__main__":
    unittest.main()
