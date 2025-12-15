# Slides Project (Markdown → reveal.js)

A minimal, fully reproducible slide system with **Markdown as source of truth**,  
**Python-governed builds**, and **GitHub Pages hosting**.

Markdown · Pandoc · reveal.js · Python 3.12 · uv · CI-ready

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
slides_project/
├── slides/
│ └── deck.md # source of truth
├── revealjs/ # vendored reveal.js (or submodule)
├── dist/
│ └── index.html # build artifact (GitHub Pages target)
├── build.py # Python-controlled build
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

---


## ⚙️ Initial Setup: Prerequisite Checklist

Step 1: Define Project Files and Structure

Before you run `uv sync` to create the isolated environment, the project needs three specific configuration files and two directories to define its identity and dependencies.

| Item | Purpose | Command Used to Create/Populate |
| :--- | :--- | :--- |
| **`.python-version`** | Specifies the exact Python version (`3.12.5`) the project requires. This ensures all developers use the same interpreter. | `echo "3.12.5" > .python-version` |
| **`pyproject.toml`** | The standard configuration file for Python projects. It names the project, sets the version, and lists the required dependencies (`rich`). | `cat > pyproject.toml << 'EOF' ... EOF` |
| **`slides/` Directory** | The folder that will hold the source-of-truth Markdown files (like `deck.md`). | `mkdir -p slides` |
| **`deck.md` File** | A placeholder for the main content file, ensuring the build process has a target. | `touch slides/deck.md` |
| **`dist/` Directory** | The folder where the final HTML build artifact (`index.html`) will be placed. | `mkdir -p dist` |


```bash
# 1. Create the three required files and directories

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

# Create the source and distribution directories
mkdir -p slides dist
touch slides/deck.md
```

Step 2: Install Python and Vendor reveal.js

This step ensures the environment dependencies are handled before the Python environment is finalized.

```bash
# 2a. Install Python 3.12.5 if you don't have it yet
# (This is managed by 'pyenv' and is instant if the version is already installed)
pyenv install --skip-existing 3.12.5

# 2b. Vendor the reveal.js assets (required by Pandoc)
git clone https://github.com/hakimel/reveal.js revealjs
```

Step 3: Create the Environment and Install Dependencies

This final step uses uv to install the packages defined in pyproject.toml into the isolated virtual environment (.venv/).

```bash
# 3. Create the perfect environment (~1 second)
# uv reads pyproject.toml and installs all dependencies into .venv/
uv sync
```

Next Steps

With the environment created, you can now run the build using uv run python build.py as detailed in the Daily Workflow section.



---

### Why These Files Are Essential (The "Why")

The project setup relies on a fundamental principle: **reproducibility**. Every file created in this step serves a specific role in ensuring that the slide system builds exactly the same way for every developer and on the CI server.

#### The Governance Files (`.python-version` & `pyproject.toml`)

These files define the environment. They act as the contract for the project.

* **`.python-version`** tells the system **which** Python interpreter (`3.12.5`) to use.
* **`pyproject.toml`** tells the dependency manager (`uv`) **what** packages to install inside the virtual environment.

Without these files, the environment cannot be built consistently.

#### The Source and Target Directories (`slides/` & `dist/`)

These are the two endpoints of our workflow:

* **`slides/`**: This is the **input** folder. It is the only place where developers should ever edit files. The core rule is: **Markdown is the source of truth.**
* **`dist/`**: This is the **output** folder. It's the destination for the final `index.html` built by Pandoc. We create it now so the build script never fails to find the target.

This structure separates the customizable source code (in `slides/`) from the automatically generated artifacts (in `dist/`).

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
Calls Pandoc
Uses reveal.js as the renderer
Writes output to dist/index.html
Can inject version, date, commit hash, etc.
PowerPoint never enters the pipeline.


One-Time reveal.js Setup
Either vendor reveal.js:

```bash
git clone https://github.com/hakimel/reveal.js revealjs
```

Or add it as a Git submodule.
After that, never touch it manually.

Perfect .gitignore
```gitignore
# Python / uv
.venv/
uv.lock.tmp
__pycache__/
*.py[cod]

# Build artifacts
dist/

# macOS
.DS_Store

# VS Code
.vscode/

# Pandoc temp files
*.log
```


| Rule | Explanation |
| :--- | :--- |
| **Markdown is source of truth** | `slides/*.md` only |
| **Never edit `dist/` manually** | Always rebuilt |
| **Always commit `uv.lock`** | Reproducibility |
| **Never commit `.venv/`** | Recreated instantly |

Daily Workflow

```bash
# Edit slides
vim slides/deck.md

# Build
uv run python build.py

# Review locally
open dist/index.html

# Commit
git add slides build.py pyproject.toml uv.lock
git commit -m "slides: update section on X"
git push
```

GitHub Pages Hosting
GitHub Pages serves dist/
CI can rebuild on every push to main
URL:

```php-template
https://<username>.github.io/<repo>
```

No servers. No runtime dependencies.

Golden Rules
Markdown only
Python controls everything
Builds must succeed from a clean clone
If it’s not reproducible, it’s a bug

```markdown
TL;DR

```bash
uv sync
edit slides/*.md
uv run python build.py
git commit
git push
```

Slides as code nothing else:

```yaml

If you want next:
- the **exact `build.py`**
- a **Pandoc command line pinned properly**
- or a **GitHub Actions workflow**

say which one.
```








