"""The private ipe_web_kit is pinned by vendor/ipe_web_kit.lock (the source is not in this public repo): installed copy = the locked kit,
a missing kit says how to install it, a different kit fails."""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import kit_lock  # noqa: E402
from helpers import REPO as _R  # noqa: E402,F401  (puts scripts/ on sys.path for indexnow)


def run(root, *args):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "kit_lock.py"), "--root", str(root), *args], capture_output=True, text=True)


class KitLock(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "vendor").mkdir()
        shutil.copy(REPO / "vendor" / "ipe_web_kit.lock", self.tmp / "vendor")

    def test_lock_format(self):
        lock = kit_lock.read_lock(REPO)
        self.assertRegex(lock["tag"], r"^v\d+\.\d+\.\d+$")
        self.assertRegex(lock["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(lock["manifest_sha256"], r"^[0-9a-f]{64}$")

    def test_installed_kit_is_the_locked_one(self):
        self.assertEqual(kit_lock.problems(REPO), [])

    def test_kit_source_is_not_tracked(self):
        out = subprocess.run(["git", "ls-files", "vendor"], capture_output=True, text=True, cwd=REPO)
        if out.returncode == 0:
            self.assertEqual([f for f in out.stdout.split() if f != "vendor/ipe_web_kit.lock"], [])

    def test_missing_kit_gives_install_instructions(self):
        r = run(self.tmp, "check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not installed", r.stderr)
        self.assertIn("scripts/kit_lock.py sync --kit", r.stderr)

    def test_other_kit_than_locked_fails(self):
        shutil.copytree(REPO / "vendor" / "ipe_web_kit", self.tmp / "vendor" / "ipe_web_kit")
        self.assertEqual(kit_lock.problems(self.tmp), [])
        lock = self.tmp / "vendor" / "ipe_web_kit.lock"
        lock.write_text(re.sub(r"commit=[0-9a-f]{40}", "commit=" + "0" * 40, lock.read_text()))
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "differs from the lock" in p])
        lock.write_text((REPO / "vendor" / "ipe_web_kit.lock").read_text())
        lock.write_text(re.sub(r"manifest_sha256=\w+", "manifest_sha256=" + "0" * 64, lock.read_text()))
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "manifest hash" in p])

    def test_edited_kit_file_fails(self):
        shutil.copytree(REPO / "vendor" / "ipe_web_kit", self.tmp / "vendor" / "ipe_web_kit")
        with open(self.tmp / "vendor" / "ipe_web_kit" / "seo.py", "a", encoding="utf-8") as f:
            f.write("\n# tampered\n")
        self.assertTrue([p for p in kit_lock.problems(self.tmp) if "changed after install" in p])

    def test_ci_installs_the_kit_and_never_deploys_it(self):
        wf = (REPO / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertIn("--exclude='vendor'", wf)
        check_job = wf.split("  deploy:")[0]
        self.assertIn("uses: ./.github/actions/ipe-web-kit", check_job)
        self.assertIn("secrets.IPE_WEB_KIT_DEPLOY_KEY", check_job)

    def test_indexnow_comes_from_the_installed_kit(self):
        import indexnow
        self.assertEqual(indexnow.find_key.__module__, "ipe_web_kit.indexnow")
        self.assertEqual(indexnow.main(["--dry-run"]), 0)


if __name__ == "__main__":
    unittest.main()
