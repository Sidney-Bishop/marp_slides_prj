# 💡 Project: Slides-as-Code

### Markdown → Pandoc → Reveal.js

A minimal, fully reproducible build system.

---

## 🗺️ Agenda

* **Overview:** Philosophy and Goals
* **Implementation:** Tools and Workflow
* **Results:** Reproducibility and Hosting

---

## 🎯 Overview: Philosophy

The core principle is **Slides are Code**.

* Markdown is the single, authoritative **source of truth**.
* No proprietary binary files (e.g., PowerPoint).
* The entire output (`dist/index.html`) is **deterministic and reproducible**.
* Everything builds from a clean clone using a Python-governed process.

---

## 🛠️ Implementation: The Build Chain

The process is orchestrated by a small, robust toolchain:

![Screenshot of the successful build output](assets/test_image.jpg){width=10%}

1. **Source:** `slides/deck.md` (Markdown)
2. **Orchestration:** `build.py` (Python + `uv` + `rich`)
3. **Engine:** **Pandoc** (Markdown $\to$ HTML)
4. **Vendor:** `revealjs/` (Presentation Assets)
5. **Output:** `dist/index.html` (Final HTML Artifact)

---

## 🚀 Results: Benefits

### A fully automated, lightweight system:

* **Local Review:** Instant builds using `uv run python build.py`.
* **Hosting:** Zero-cost deployment via **GitHub Pages**.
* **Maintenance:** Easy to update and collaborate with plain text files.
* **CI-Ready:** Automatic rebuild and deploy on every commit via **GitHub Actions**.

---


# 📚 References & Further Reading

* **Pandoc Documentation:** The universal document converter.
* [https://pandoc.org](https://pandoc.org)

* **Reveal.js Documentation:** HTML presentation framework.
* [https://revealjs.com](https://revealjs.com)

* **uv Documentation:** The fast Python package installer and resolver.
* [https://astral.sh/uv](https://astral.sh/uv)

---

# What's Next?

### Automate the pipeline!

Let's implement the **GitHub Actions Workflow** to deploy this deck live.

