import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pva_lint", ROOT / "cli.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def test_empty_is_not_ready(self):
        r = MODULE.scan_repo(self.path)
        self.assertEqual(r["structural_score"], 0)
        self.assertEqual(len(r["carencias"]), 6)

    def test_git_is_not_open_source_proof(self):
        (self.path / ".git").mkdir()
        r = MODULE.scan_repo(self.path)
        self.assertEqual(r["checks"]["codigo"]["state"], "missing")
        self.assertFalse(r["public_access_verified"])

    def test_empty_data_is_not_dataset(self):
        (self.path / "data").mkdir()
        (self.path / "data.csv").touch()
        self.assertEqual(MODULE.scan_repo(self.path)["checks"]["datos"]["state"], "missing")

    def test_reproduce_comment_and_assignment_not_target(self):
        make = self.path / "Makefile"
        for text in ("# please reproduce this\n", "reproduce := false\n"):
            make.write_text(text)
            self.assertEqual(MODULE.scan_repo(self.path)["checks"]["reproduce"]["state"], "missing")
        make.write_text("reproduce:\n\t@echo ok\n")
        self.assertEqual(MODULE.scan_repo(self.path)["checks"]["reproduce"]["state"], "observed")

    def test_all_presence_is_not_validation(self):
        for name, content in {"README.md": "https://doi.org/10.1234/example).",
                              "data.csv": "a\n1\n", "code.py": "# source\n",
                              "Dockerfile": "FROM scratch\n",
                              "Makefile": "reproduce:\n\tfalse\n",
                              "plot_data.py": "# not executed\n"}.items():
            (self.path / name).write_text(content)
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
            r = MODULE.scan_repo(self.path)
        self.assertEqual(r["structural_score"], 1)
        self.assertEqual(r["checks"]["doi"]["identifiers"], ["10.1234/example"])
        for key in ("public_access_verified", "reproduction_executed",
                    "scientific_claims_validated", "network_used"):
            self.assertFalse(r[key])
        self.assertEqual(len(r["checks"]["docker"]["evidence"][0]["sha256"]), 64)

    def test_symlinks_not_counted(self):
        (self.path / "README.md").symlink_to(ROOT / "README.md")
        (self.path / "data").symlink_to(ROOT)
        self.assertEqual(MODULE.scan_repo(self.path)["observed_checks"], 0)

    def test_cli_json_and_missing_path(self):
        good = subprocess.run([sys.executable, str(ROOT / "cli.py"), "--path", str(self.path), "--json"],
                              capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        self.assertEqual(json.loads(good.stdout)["schema"], "pva.artifact-readiness/v1")
        bad = subprocess.run([sys.executable, str(ROOT / "cli.py"), "--path", str(self.path / "absent")],
                             capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)

    def test_deterministic(self):
        (self.path / "code.py").write_text("# stable")
        self.assertEqual(MODULE.scan_repo(self.path), MODULE.scan_repo(self.path))


if __name__ == "__main__":
    unittest.main()
