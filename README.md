# Slides Project (Markdown → HTML via Marp)

A minimal, fully reproducible slide system with **Markdown as source of truth**,  
**Python-governed builds**, and **GitHub Pages hosting**.

Markdown · Marp · Python 3.12 · uv · CI-ready

---

## Project Philosophy

- **Slides are code**
- Markdown is the only authoritative source
- Output is deterministic and reproducible
- No PowerPoint, no binaries, no manual tweaking
- Everything builds from a clean clone

---



## Repo Layout

```text
marp_slides_prj/
├── .github/workflows/
│   └── build.yml          # CI/CD pipeline (GitHub Actions)
├── assets/                # Static assets (images, etc.)
│   ├── CRISP-DM_Process_Diagram.png
│   └── test_image.jpg
├── slides/                # Source of truth
│   └── deck.md           # Main slide content
├── .venv/                 # Python virtual environment (gitignored)
├── .python-version        # Python version specification
├── .gitignore            # Git ignore rules
├── build.py              # Python-controlled build script
├── package.json          # Node.js configuration
├── package-lock.json     # Node.js lock file
├── pyproject.toml        # Python project configuration
├── uv.lock               # Python dependency lock file
└── README.md             # This file
```

**Live Demo:** https://sidney-bishop.github.io/marp_slides_prj/




## ⚙️ Initial Setup: Prerequisite Checklist

Step 1: Define Project Files and Structure

Before you run `uv sync` to create the isolated environment, the project needs three specific configuration files and two directories to define its identity and dependencies.

| Item | Purpose | Command Used to Create/Populate |
| :--- | :--- | :--- |
| **`.python-version`** | Specifies the exact Python version (`3.12.5`) the project requires. This ensures all developers use the same interpreter. | `echo "3.12.5" > .python-version` |
| **`pyproject.toml`** | The standard configuration file for Python projects. It names the project, sets the version, and lists the required dependencies (`rich`). | `cat > pyproject.toml << 'EOF' ... EOF` |
| **`slides/` Directory** | The folder that will hold the source-of-truth Markdown files (like `deck.md`). | `mkdir -p slides` |
| **`deck.md` File** | A placeholder for the main content file, ensuring the build process has a target. | `touch slides/deck.md` |
| **`dist/` Directory** | Build output directory (gitignored). Created locally for testing, built fresh in CI for deployment. | `mkdir -p dist` |
| **`package.json`** | Node.js configuration for Marp (created by npm). | `npm init -y` |


```bash
# 1. Create the required files and directories

# Defines the Python version (3.12.5) for pyenv
echo "3.12.5" > .python-version

# Defines project metadata and the 'rich' dependency
cat > pyproject.toml << 'EOF'
[project]
name = "slides_project"
version = "0.1.0"
description = "Markdown-driven slides with Python governance"
requires-python = ">=3.12,<3.13"

dependencies = [
    "rich>=13.7",     # logging / diagnostics for build.py
]
EOF

# Initialize npm for Marp (optional - npx works without this)
npm init -y

# Create the source, assets, and distribution directories
mkdir -p slides assets dist
touch slides/deck.md

# Note: 'dist/' is gitignored and built fresh in CI environment
```


## Step 2: Install Python and Verify Environment

This step ensures the environment dependencies are handled before the Python environment is finalized.

```bash

# 2a. Install Python 3.12.5 if you don't have it yet
pyenv install --skip-existing 3.12.5

# 2b. Verify Node.js availability
# Marp runs via npx and requires Node.js for consistent builds
node --version || echo "Note: Node.js is required. Install from https://nodejs.org/"

# Note: GitHub Actions automatically sets up both Python and Node.js in CI
```


---

### Why These Files Are Essential (The "Why")

The project setup relies on a fundamental principle: **reproducibility**. Every file serves a specific role in ensuring that the slide system builds exactly the same way for every developer and on the CI server.

#### The Governance Files (`.python-version` & `pyproject.toml`)

These files define the environment. They act as the contract for the project.

* **`.python-version`** tells the system **which** Python interpreter (`3.12.5`) to use.
* **`pyproject.toml`** tells the dependency manager (`uv`) **what** packages to install inside the virtual environment.
* **`package.json`** defines Node.js configuration for Marp (ensuring consistent builds across environments).

Without these files, the environment cannot be built consistently.

#### The Source and Target Directories (`slides/` & `dist/`)

These are the two endpoints of our workflow:

* **`slides/`**: This is the **input** folder. It is the only place where developers should ever edit files. The core rule is: **Markdown is the source of truth.**
* **`dist/`**: This is the **output** folder. It's where the final `index.html` is built by **Marp**. This directory is gitignored and built fresh in the CI environment, then automatically deployed to GitHub Pages.

This structure separates the customizable source code (in `slides/`) from the automatically generated artifacts (in `dist/`), with GitHub Actions handling the build and deployment pipeline.

---

Writing Slides:
Slides live in plain Markdown.

```markdown
# Title Slide

Subtitle here

---

## Second Slide

- Bullet one
- Bullet two
```

Rules:
--- = new slide
No formatting magic outside Markdown
No edits directly in dist/

```bash
uv run python build.py
```

What the build does:
Calls Marp (Markdown Presentation Ecosystem)
Generates reveal.js-compatible HTML slides
Writes output to dist/index.html
Can inject version, date, commit hash, etc.
PowerPoint never enters the pipeline.

**Note:** The build also runs automatically via GitHub Actions on every `git push`, 
deploying your slides to https://sidney-bishop.github.io/marp_slides_prj/




Perfect .gitignore
```gitignore
# Python
.venv/
__pycache__/
*.pyc

# Node
node_modules/
npm-debug.log*

# Build artifacts
dist/

# macOS
.DS_Store

# Environment files
.env

```


| Rule | Explanation |
| :--- | :--- |
| **Markdown is source of truth** | `slides/*.md` only |
| **Never edit `dist/` manually** | Always rebuilt |
| **Always commit `uv.lock`** | Reproducibility |
| **Never commit `.venv/`** | Recreated instantly |
| **Always commit `package-lock.json`** | Pins exact Marp/npm versions for reproducibility |





## Daily Workflow

```bash
# 1. Edit your slides
vim slides/deck.md

# 2. (Optional) Build locally to preview
uv run python build.py
npx serve dist  # or: open dist/index.html

# 3. Commit source changes only
git add slides/deck.md
git commit -m "slides: update [section/topic]"

# 4. Push to trigger automated deployment
git push


GitHub Pages Hosting
GitHub Pages serves dist/
CI can rebuild on every push to main
URL:

```php-template
https://<username>.github.io/<repo>
```


## Golden Rules

- **Markdown only** - Source of truth
- **Python controls everything** - Build automation
- **Builds must succeed from a clean clone** - Reproducibility
- **If it's not reproducible, it's a bug** - Quality guarantee

## TL;DR

```bash
# Setup once
uv sync

# Daily workflow
edit slides/deck.md
git add slides/deck.md
git commit -m "update slides"
git push  # ← Triggers GitHub Actions auto-deploy!
```





## 🔍 Local Preview (GitHub Pages–Accurate)

This project does **not** use a live development server.

GitHub Pages serves **static files only**, so local preview must do the same.

### Correct local preview

After building:

npx serve dist

or:

python -m http.server --directory dist 8000

Then open:

http://localhost:8000

This is byte-for-byte equivalent to GitHub Pages.

### Do NOT use Marp’s dev server

marp --serve

Marp’s dev server renders Markdown directly, ignores `dist/`, and does not reflect
GitHub Pages behavior. If it works in `dist/` but fails under `marp serve`,
the server is the problem.


## 🌐 Live Deployment

Your slides are automatically built and deployed via **GitHub Actions**:

[![GitHub Pages Deployment](https://github.com/Sidney-Bishop/marp_slides_prj/actions/workflows/build.yml/badge.svg)](https://github.com/Sidney-Bishop/marp_slides_prj/actions/workflows/build.yml)

**Live URL:** https://sidney-bishop.github.io/marp_slides_prj/

Access this URL from any device to present your slides. Updates automatically within 2 minutes of pushing changes.












