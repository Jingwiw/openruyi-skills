import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("docker_runner", ROOT / "skills/docker-disposable-experiment/scripts/run.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
CID = "c" * 64
IMAGE = "example.invalid/image@sha256:" + "a" * 64


class RunnerTests(unittest.TestCase):
    def simulate(self, exit_code=0, cleanup_fail=False, create_fail=False, timed_out=False, ps_fail=False):
        calls = []
        def docker(argv, **kwargs):
            calls.append(argv)
            verb = argv[1]
            code, out, err = 0, b"", b""
            if verb == "create":
                code, out = (1, b"") if create_fail else (0, (CID + "\n").encode())
            elif verb == "start":
                if timed_out:
                    raise subprocess.TimeoutExpired(argv, 1, output=b"partial", stderr=b"waiting")
                code, out, err = exit_code, b"test-output\n", b"test-error\n"
            elif verb == "inspect":
                out = json.dumps({"Running": timed_out, "ExitCode": exit_code}).encode()
            elif verb == "rm":
                code = 1 if cleanup_fail else 0
            elif verb == "ps":
                code = 1 if ps_fail else 0
                out = (CID + "\n").encode() if cleanup_fail else b""
            return subprocess.CompletedProcess(argv, code, out, err)
        with tempfile.TemporaryDirectory() as t:
            inputs = Path(t) / "input"; inputs.mkdir()
            output = Path(t) / "output"
            with patch.object(runner.subprocess, "run", side_effect=docker):
                result = runner.execute(IMAGE, "linux/amd64", inputs, output, ["sh", "/input/test.sh"])
            data = json.loads((output / "result.json").read_text())
            if not create_fail:
                self.assertTrue((output / "stdout.bin").exists())
                self.assertTrue((output / "stderr.bin").exists())
            return result, data, calls

    def test_success_cleanup(self):
        code, data, calls = self.simulate()
        self.assertEqual(code, 0)
        self.assertTrue(data["cleanup_verified"])
        self.assertIn(["docker", "rm", "--force", CID], calls)
        self.assertNotIn("--privileged", calls[0])

    def test_failure_preserves_exit_and_cleans(self):
        code, data, _ = self.simulate(exit_code=7)
        self.assertEqual(code, 7)
        self.assertEqual(data["experiment_exit"], 7)
        self.assertTrue(data["cleanup_verified"])

    def test_cleanup_failure_does_not_hide_experiment(self):
        code, data, _ = self.simulate(exit_code=7, cleanup_fail=True)
        self.assertEqual(code, 1)
        self.assertEqual(data["experiment_exit"], 7)
        self.assertFalse(data["cleanup_verified"])

    def test_create_failure_reconciles_name(self):
        code, data, calls = self.simulate(create_fail=True)
        self.assertEqual(code, 1)
        self.assertIsNone(data["experiment_exit"])
        self.assertTrue(any("name=^/skill-experiment-" in " ".join(c) for c in calls))

    def test_timeout_not_product_exit(self):
        code, data, _ = self.simulate(timed_out=True)
        self.assertEqual(code, 1)
        self.assertTrue(data["runner_timeout"])
        self.assertIsNone(data["experiment_exit"])
        self.assertTrue(data["cleanup_verified"])

    def test_daemon_error_not_absence(self):
        code, data, _ = self.simulate(ps_fail=True)
        self.assertEqual(code, 1)
        self.assertFalse(data["cleanup_verified"])

    def test_refuses_mutable_image(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):
                runner.execute("example:latest", "linux/amd64", t, Path(t) / "out", ["true"])

    def test_refuses_existing_result_directory(self):
        with tempfile.TemporaryDirectory() as t:
            output = Path(t) / "out"; output.mkdir()
            with self.assertRaises(FileExistsError):
                runner.execute(IMAGE, "linux/amd64", t, output, ["true"])


if __name__ == "__main__":
    unittest.main()
