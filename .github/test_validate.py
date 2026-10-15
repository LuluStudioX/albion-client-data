import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "validate.py")
ROOT = os.path.dirname(HERE)
XML = b"<a/>"


def entry(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


class ValidateTree(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        shutil.copytree(os.path.join(ROOT, "gamedata"), os.path.join(self.tmp, "gamedata"))
        for f in ("VERSION", "manifest.json"):
            shutil.copy(os.path.join(ROOT, f), self.tmp)
        self.man = json.load(open(os.path.join(self.tmp, "manifest.json"), encoding="utf-8"))

    def run_validate(self):
        with open(os.path.join(self.tmp, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(self.man, f)
        return subprocess.run([sys.executable, SCRIPT], cwd=self.tmp, capture_output=True, text=True)

    def add_nested(self):
        d = os.path.join(self.tmp, "gamedata", "cluster")
        os.makedirs(d)
        open(os.path.join(d, "world.xml"), "wb").write(XML)

    def test_current_tree_passes(self):
        self.assertEqual(self.run_validate().returncode, 0)

    def test_nested_file_passes(self):
        self.add_nested()
        self.man["files"]["cluster/world.xml"] = entry(XML)
        r = self.run_validate()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_listed_but_absent_fails(self):
        self.man["files"]["cluster/world.xml"] = entry(XML)
        r = self.run_validate()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("listed but absent: ['cluster/world.xml']", r.stdout)

    def test_nested_unlisted_fails(self):
        self.add_nested()
        r = self.run_validate()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unlisted: ['cluster/world.xml']", r.stdout)

    def test_parent_key_fails(self):
        self.man["files"]["../x.xml"] = entry(XML)
        r = self.run_validate()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not a relative path", r.stdout)

    def test_absolute_key_fails(self):
        self.man["files"]["/x.xml"] = entry(XML)
        r = self.run_validate()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not a relative path", r.stdout)


if __name__ == "__main__":
    unittest.main()
