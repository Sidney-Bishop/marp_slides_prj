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

![Screenshot of the successful build output](assets/test_image.jpg)

<div style="text-align: center; font-size: 0.8em; color: #666;">
*Successful build output showing 10KB file size*
</div>

1. **Source:** `slides/deck.md` (Markdown)
2. **Orchestration:** `build.py` (Python + `uv` + `rich`)
3. **Engine:** **Pandoc** (Markdown → HTML)
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

---

# Questions?

## Thank you! 🎉

<style>
.reveal .slides {
    text-align: left;
}

.reveal h1 {
    color: #e7ad52;
    text-align: center;
}

.reveal h2 {
    color: #e7ad52;
    border-bottom: 2px solid #e7ad52;
    padding-bottom: 10px;
}

.reveal img {
    max-height: 300px;
    border: 2px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.reveal .slide-number {
    font-size: 12px;
}

.build-info {
    position: absolute;
    bottom: 10px;
    right: 10px;
    font-size: 0.6em;
    color: #666;
    font-family: monospace;
}
</style>

<div class="build-info">
Built: $build-time$ | Commit: $commit-hash$
</div>