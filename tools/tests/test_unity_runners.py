import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

import run_unity_build
import run_unity_tests


class UnityRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.unity = self.directory / "Unity.exe"
        self.unity.touch()
        self.output = self.directory / "output"
        self.stderr = io.StringIO()
        self.patch("sys.stderr", self.stderr)
        # main() configures stdout; a mock avoids changing the test runner's stream.
        self.patch("sys.stdout", Mock())
        for module in (run_unity_tests, run_unity_build):
            self.patch_object(module, "UNITY_EXE", self.unity)
            self.patch_object(module, "OUTPUT", self.output)
            self.patch_object(module, "project_is_open", Mock(return_value=False))
        self.exe = self.directory / "TapDoc.exe"
        self.exe.touch()
        self.patch_object(run_unity_build, "EXE_PATH", self.exe)

    def patch(self, target, value):
        patcher = patch(target, value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def patch_object(self, target, name, value):
        patcher = patch.object(target, name, value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_tests_missing_unity(self):
        missing = self.directory / "missing.exe"
        with patch.object(run_unity_tests, "UNITY_EXE", missing), \
                patch("sys.argv", ["run_unity_tests.py", "editmode"]), \
                patch("run_unity_tests.subprocess.run") as run:
            self.assertEqual(run_unity_tests.main(), 2)
        run.assert_not_called()
        self.assertEqual(self.stderr.getvalue(), f"Không tìm thấy Unity: {missing}\n")

    def test_build_missing_unity(self):
        missing = self.directory / "missing.exe"
        with patch.object(run_unity_build, "UNITY_EXE", missing), \
                patch("run_unity_build.subprocess.run") as run:
            self.assertEqual(run_unity_build.build_windows(), 2)
        run.assert_not_called()
        self.assertEqual(self.stderr.getvalue(), f"Không tìm thấy Unity: {missing}\n")

    def test_tests_timeout(self):
        with patch("sys.argv", ["run_unity_tests.py", "editmode", "--timeout", "5"]), \
                patch("run_unity_tests.subprocess.run", side_effect=
                      subprocess.TimeoutExpired(cmd="unity", timeout=5)) as run:
            self.assertEqual(run_unity_tests.main(), 2)
        self.assertEqual(run.call_args.kwargs["timeout"], 5)
        self.assertIn("quá 5 giây", self.stderr.getvalue())

    def test_build_timeout(self):
        with patch("sys.argv", ["run_unity_build.py", "--timeout", "5"]), \
                patch("run_unity_build.subprocess.run", side_effect=
                      subprocess.TimeoutExpired(cmd="unity", timeout=5)) as run:
            self.assertEqual(run_unity_build.main(), 2)
        self.assertEqual(run.call_args.kwargs["timeout"], 5)
        self.assertIn("quá 5 giây", self.stderr.getvalue())

    def test_tests_timeout_forwarded_and_stale_files_removed(self):
        self.output.mkdir()
        log_path = self.output / "editmode.log"
        xml_path = self.output / "editmode.xml"
        log_path.write_text("stale log", encoding="utf-8")
        xml_path.write_text("stale XML", encoding="utf-8")
        observed = []

        def run_unity(command, **kwargs):
            actual_log = Path(command[command.index("-logFile") + 1])
            observed.append((actual_log, actual_log.exists(), xml_path.exists()))
            xml_path.write_text('<test-run result="Passed"><test-case result="Passed" /></test-run>',
                                encoding="utf-8")
            return subprocess.CompletedProcess(command, 0)

        with patch("sys.argv", ["run_unity_tests.py", "editmode", "--timeout", "7"]), \
                patch("run_unity_tests.subprocess.run", side_effect=run_unity) as run:
            self.assertEqual(run_unity_tests.main(), 0)
        self.assertEqual(run.call_args.kwargs["timeout"], 7)
        self.assertEqual(observed, [(log_path, False, False)])

    def test_build_timeout_forwarded(self):
        with patch("sys.argv", ["run_unity_build.py", "--timeout", "7"]), \
                patch("run_unity_build.subprocess.run", return_value=
                      subprocess.CompletedProcess("unity", 0)) as run:
            self.assertEqual(run_unity_build.main(), 0)
        self.assertEqual(run.call_args.kwargs["timeout"], 7)

    def test_default_timeouts(self):
        for module, argv, expected in (
                (run_unity_tests, ["run_unity_tests.py", "editmode"], 1800),
                (run_unity_build, ["run_unity_build.py"], 3600)):
            with self.subTest(module=module.__name__), patch("sys.argv", argv), \
                    patch.object(module.subprocess, "run", return_value=
                                 subprocess.CompletedProcess("unity", 0)) as run:
                module.main()
                self.assertEqual(run.call_args.kwargs["timeout"], expected)

    def test_launch_does_not_use_build_timeout(self):
        with patch("sys.argv", ["run_unity_build.py", "--launch", "1600x720", "--timeout", "7"]), \
                patch("run_unity_build.subprocess.Popen") as launch, \
                patch("run_unity_build.subprocess.run") as run:
            self.assertEqual(run_unity_build.main(), 0)
        run.assert_not_called()
        launch.assert_called_once()
        self.assertNotIn("timeout", launch.call_args.kwargs)

    def test_launch_needs_only_the_built_exe(self):
        # Mở bản đã build không cần Unity Editor: thiếu Unity.exe vẫn mở được TapDoc.exe.
        with patch.object(run_unity_build, "UNITY_EXE", self.directory / "missing.exe"), \
                patch("run_unity_build.subprocess.Popen") as launch:
            self.assertEqual(run_unity_build.launch_windowed("1600x720"), 0)
        launch.assert_called_once()

    def test_unreadable_results(self):
        corrupt = self.directory / "corrupt.xml"
        corrupt.write_text("<not xml", encoding="utf-8")
        for path in (corrupt, self.directory / "missing.xml", self.directory):
            with self.subTest(path=path), redirect_stdout(io.StringIO()) as output:
                self.assertEqual(run_unity_tests.summarize(path, "EditMode"), 2)
                self.assertEqual(output.getvalue(), f"Không đọc được kết quả test: {path}\n")


if __name__ == "__main__":
    unittest.main()
