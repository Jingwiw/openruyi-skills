import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate import frontmatter, validate_repo, validate_skill
from catalog import render, START, END


class SkillsTests(unittest.TestCase):
    def fixture(self, root, body="Useful knowledge.", extra=""):
        d = Path(root) / "sample"
        d.mkdir()
        (d / "SKILL.md").write_text('---\nname: sample\ndescription: "A useful sample"\nmetadata:\n  kind: knowledge\n' + extra + '---\n\n' + body)
        return d

    def test_active_format(self):
        paths, errors = validate_repo(ROOT)
        self.assertTrue(paths)
        self.assertEqual(errors, [])

    def test_each_skill_copies_alone(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name), tempfile.TemporaryDirectory() as t:
                dest = Path(t) / path.parent.name
                shutil.copytree(path.parent, dest)
                self.assertEqual(validate_skill(dest), [])

    def test_relocate_beside_specs(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "openRuyi"
            (root / "SPECS").mkdir(parents=True)
            shutil.copytree(ROOT / "skills", root / "skills")
            self.assertEqual(validate_repo(root)[1], [])

    def test_reject_missing_reference(self):
        with tempfile.TemporaryDirectory() as t:
            d = self.fixture(t, "[missing](references/no.md)")
            self.assertTrue(any("missing local reference" in e for e in validate_skill(d)))

    def test_reject_hidden_sibling_dependency(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "common.md").write_text("exists but is not bundled")
            d = self.fixture(t, "[common](../common.md)")
            self.assertTrue(any("escapes" in e for e in validate_skill(d)))

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as t:
            d = self.fixture(t)
            (d / "alias.md").symlink_to(d / "SKILL.md")
            self.assertTrue(any("symlink" in e for e in validate_skill(d)))

    def test_reject_duplicate_yaml_key(self):
        with tempfile.TemporaryDirectory() as t:
            d = self.fixture(t, extra="name: sample\n")
            self.assertTrue(any("duplicate" in e for e in validate_skill(d)))

    def test_reject_name_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            d = self.fixture(t)
            d.rename(Path(t) / "different")
            self.assertTrue(validate_skill(Path(t) / "different"))

    def test_knowledge_does_not_require_execution(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(validate_skill(self.fixture(t, "Distinguish a build result from runtime evidence.")), [])

    def test_catalog_is_derived(self):
        actual = (ROOT / "README.md").read_text().split(START)[1].split(END)[0].strip()
        self.assertEqual(actual, render(ROOT))

    def test_scenario_references_exist(self):
        cases = json.loads((ROOT / "tests/scenarios.json").read_text())
        names = {frontmatter(p)[0]["name"] for p in (ROOT / "skills").glob("*/SKILL.md")}
        ids = set()
        for case in cases:
            self.assertNotIn(case["id"], ids)
            ids.add(case["id"])
            self.assertTrue(set(case["skills"]) <= names)
            self.assertTrue(case["request"] and case["must_observe"] and case["must_not"])


if __name__ == "__main__":
    unittest.main()
