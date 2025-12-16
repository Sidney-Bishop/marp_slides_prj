#!/usr/bin/env python3
"""
build.py - Simple slide builder
"""
import subprocess
import shutil
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.cmd}")
        logger.error(f"Return code: {e.returncode}")
        return False

def main():
    try:
        logger.info("Starting build process")

        # Clean dist
        dist = Path("dist")
        if dist.exists():
            logger.info("Cleaning dist directory")
            shutil.rmtree(dist)
        dist.mkdir()
        logger.info("Created dist directory")

        # Copy assets
        assets = Path("assets")
        if assets.exists():
            logger.info("Copying assets")
            shutil.copytree(assets, dist / "assets", dirs_exist_ok=True)
            logger.info("Assets copied")

        # Build with Marp (enable HTML and allow local files)
        # NOTE: --allow-local-files is added to fix image path issue
        logger.info("Building slides with Marp")
        marp_cmd = ["npx", "@marp-team/marp-cli", "--html", "--allow-local-files", "slides/deck.md", "-o", "dist/index.html"]
        
        if not run_command(marp_cmd):
            return False
            
        logger.info("Marp build complete")
        logger.info("✅ Built: dist/index.html")
        logger.info("Build process complete")
        return True
        
    except Exception as e:
        logger.error(f"Build process error: {e}")
        return False

if __name__ == "__main__":
    if main():
        print("✅ Build successful. Ready to commit and push.")
    else:
        print("❌ Build failed! Fix issues before committing.")
        sys.exit(1)