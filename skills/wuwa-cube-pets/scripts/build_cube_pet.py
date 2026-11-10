#!/usr/bin/env python3
"""Build the repository's v1 cube package from five original Tappo PNG layers."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from PIL import Image


# Zero-based head/body pairs, in the v1 row order.
STATES = {
    "idle": [(0, 0), (0, 0), (0, 0), (1, 0), (1, 0), (0, 0)],
    "running-right": [(0, 0), (0, 1), (0, 0), (0, 2), (0, 0), (1, 1), (1, 0), (0, 2)],
    "running-left": [(0, 0), (0, 2), (0, 0), (0, 1), (0, 0), (1, 2), (1, 0), (0, 1)],
    "waving": [(0, 0), (0, 1), (0, 0), (0, 1)],
    "jumping": [(0, 0), (0, 1), (1, 0), (0, 2), (0, 0)],
    "failed": [(0, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 0)],
    "waiting": [(0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0)],
    "running": [(0, 0), (0, 1), (0, 0), (0, 2), (1, 0), (0, 0)],
    "review": [(0, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 0)],
}
CELL = (192, 208)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_layer(path):
    with Image.open(path) as image:
        require(image.format == "PNG", f"PNG required: {path}")
        require(image.size == (560, 560), f"Expected a 560x560 source layer: {path}")
        layer = image.convert("RGBA")
    alpha = layer.getchannel("A")
    require(alpha.getextrema()[0] == 0 and alpha.getbbox(), f"Transparent layer required: {path}")
    return layer


def write_animation(frames, durations, destination):
    with tempfile.TemporaryDirectory(prefix="cube-webp-") as scratch:
        command = ["webpmux"]
        for index, (frame, duration) in enumerate(zip(frames, durations)):
            png = Path(scratch) / f"{index}.png"
            webp = png.with_suffix(".webp")
            frame.save(png)
            subprocess.run(
                ["cwebp", "-quiet", "-lossless", "-exact", "-m", "6", str(png), "-o", str(webp)],
                check=True,
            )
            command.extend(["-frame", str(webp), f"+{duration}+0+0+0-b"])
        subprocess.run(
            command + ["-loop", "0", "-bgcolor", "0,0,0,0", "-o", str(destination)],
            check=True, capture_output=True, text=True,
        )
    with Image.open(destination) as animation:
        require(animation.size == CELL, f"Wrong preview size: {destination}")
        require(animation.n_frames == len(frames), f"Wrong frame count: {destination}")
        require(animation.info.get("loop") == 0, f"Wrong loop setting: {destination}")
        for index, (frame, duration) in enumerate(zip(frames, durations)):
            animation.seek(index)
            decoded = animation.convert("RGBA")
            require(decoded.tobytes() == frame.tobytes(), f"RGBA mismatch: {destination}, frame {index}")
            require(animation.info.get("duration") == duration, f"Timing mismatch: {destination}, frame {index}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--name", required=True, help="Codex display name, e.g. 치사 새알심")
    parser.add_argument("--output", type=Path, required=True, help="New staging directory; must not exist")
    args = parser.parse_args()
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*-cube", args.id), "ID must be a lowercase slug ending in -cube")
    require(args.name.strip(), "Display name is required")
    require(not args.output.exists() and not args.output.is_symlink(), "Output already exists; choose a new staging directory")
    for command in ("cwebp", "webpmux"):
        require(shutil.which(command), f"Missing executable: {command}")
    heads = [read_layer(args.source / f"head{i}.png") for i in (1, 2)]
    bodies = [read_layer(args.source / f"body{i}.png") for i in (1, 2, 3)]
    poses = {}
    for head in range(2):
        for body in range(3):
            composed = Image.alpha_composite(bodies[body], heads[head])
            scaled = composed.resize((192, 192), Image.Resampling.LANCZOS)
            frame = Image.new("RGBA", CELL)
            frame.alpha_composite(scaled, (0, 8))
            poses[(head, body)] = frame

    args.output.mkdir(parents=True)
    pet_dir = args.output / "pets" / args.id
    preview_dir = args.output / "docs" / args.id
    pet_dir.mkdir(parents=True)
    preview_dir.mkdir(parents=True)
    atlas = Image.new("RGBA", (1536, 1872))
    for row, sequence in enumerate(STATES.values()):
        for column, pose in enumerate(sequence):
            atlas.paste(poses[pose], (column * CELL[0], row * CELL[1]))
    atlas_path = pet_dir / "spritesheet.png"
    atlas.save(atlas_path)
    with Image.open(atlas_path) as saved:
        require(saved.mode == "RGBA" and saved.size == atlas.size, "Wrong atlas format")
        for row, sequence in enumerate(STATES.values()):
            for column in range(8):
                x, y = column * CELL[0], row * CELL[1]
                cell = saved.crop((x, y, x + CELL[0], y + CELL[1]))
                expected = poses[sequence[column]] if column < len(sequence) else Image.new("RGBA", CELL)
                require(cell.tobytes() == expected.tobytes(), f"Atlas cell mismatch: {row}, {column}")

    name = args.name.strip()
    manifest = {
        "id": args.id,
        "displayName": name,
        "description": f"Wuwa Tappo 원본 눈·손 동작을 사용하는 {name}",
        "spriteVersionNumber": 1,
        "spritesheetPath": "spritesheet.png",
    }
    (pet_dir / "pet.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_animation([poses[STATES["idle"][i]] for i in (0, 3, 5)], [500, 280, 320], preview_dir / "idle.webp")
    write_animation([poses[p] for p in STATES["running"]], [120] * 5 + [220], preview_dir / "running.webp")
    print(json.dumps({"output": str(args.output.resolve()), "id": args.id, "atlas_cells_checked": 72, "used_frames": 57, "preview_frames_checked": 9, "validation": "passed"}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Build failed: {error}") from error
