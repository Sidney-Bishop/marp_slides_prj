#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path

# Clean and create dist
dist = Path("dist")
if dist.exists():
    shutil.rmtree(dist)
dist.mkdir()

# Build slides
cmd = [
    "pandoc", "slides/deck.md",
    "-t", "revealjs",
    "-o", "dist/index.html",
    "--standalone",
    "--slide-level=2",
    "-V", "revealjs-url=revealjs",
    "-V", "theme=black",
    "--extract-media=dist",
    "--resource-path=.:slides:assets",
]

subprocess.run(cmd, check=True)

# Copy assets if they exist
assets = Path("assets")
if assets.exists():
    shutil.copytree(assets, dist / "assets", dirs_exist_ok=True)

print("✅ Built: dist/index.html")