"""Run with python3 tests/test_install.py; only temporary directories are used."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="wuwa-pets-test-") as temporary:
    root = Path(temporary)
    checkout = root / "repo with spaces"
    checkout.mkdir()
    shutil.copyfile(repo / "install.sh", checkout / "install.sh")
    shutil.copytree(repo / "pets", checkout / "pets")
    codex_dir = root / "custom codex home"
    environment = {**os.environ, "CODEX_HOME": str(codex_dir)}

    def run(*arguments, input_text=None, success=True):
        result = subprocess.run(
            ["sh", str(checkout / "install.sh"), *arguments],
            input=input_text, text=True, capture_output=True, cwd=root,
            env=environment,
        )
        assert (result.returncode == 0) == success, result.stdout + result.stderr
        return result.stdout

    assert run("--list").splitlines() == ["aemeath-cube", "chisa-cube"]
    run(input_text="0\n")
    for invalid in ("../outside", "unknown", "--unknown"):
        run(invalid, success=False)
    run(input_text="999\n", success=False)
    run(input_text="", success=False)
    assert not codex_dir.exists()

    run(input_text="2\n")
    installed = codex_dir / "pets"
    assert sorted(path.name for path in installed.iterdir()) == ["chisa-cube"]
    run("aemeath-cube")
    for pet_id in ("aemeath-cube", "chisa-cube"):
        target = installed / pet_id
        assert sorted(path.name for path in target.iterdir()) == ["pet.json", "spritesheet.png"]
        assert json.loads((target / "pet.json").read_text())["id"] == pet_id
        for filename in ("pet.json", "spritesheet.png"):
            assert (target / filename).read_bytes() == (repo / "pets" / pet_id / filename).read_bytes()

    manifest = installed / "chisa-cube" / "pet.json"
    manifest.write_text("user-customized file")
    run("chisa-cube")
    run("--all")
    assert manifest.read_text() == "user-customized file"

    environment["CODEX_HOME"] = str(root / "all pets")
    run(input_text="a\n")
    assert sorted(path.name for path in (root / "all pets" / "pets").iterdir()) == ["aemeath-cube", "chisa-cube"]

    environment["CODEX_HOME"] = str(root / "missing file")
    (checkout / "pets/chisa-cube/spritesheet.png").unlink()
    run("--all", success=False)
    assert not (root / "missing file").exists()

print("Installer checks passed.")
