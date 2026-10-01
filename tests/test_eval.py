import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prepare_eval import prepare
from validate import frontmatter


class EvalTests(unittest.TestCase):
    def test_only_description_changes(self):
        with tempfile.TemporaryDirectory() as t:
            output = Path(t) / "eval"
            self.assertEqual(prepare(ROOT, output), 4)
            for p in (output / "variants").glob("*/skills/*/SKILL.md"):
                source = ROOT / "skills" / p.parent.name / "SKILL.md"
                a, abody = frontmatter(source)
                b, bbody = frontmatter(p)
                self.assertEqual(abody, bbody)
                a.pop("description"); b.pop("description")
                self.assertEqual(a, b)
            self.assertTrue(json.loads((output / "sha256.json").read_text()))

    def test_existing_eval_not_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(FileExistsError):
                prepare(ROOT, t)


if __name__ == "__main__":
    unittest.main()
