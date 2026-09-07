"""Build the coolipy documentation site into ``html/coolipy/``.

This script regenerates the static pdoc3 API reference with the custom
``docs/templates`` overrides (SEO/social/LLM metadata, cleaned-up title) and
then writes the search-engine + LLM discovery assets next to the HTML:

* ``sitemap.xml`` — generated from the actual output pages (cannot drift)
* ``robots.txt``   — copied from ``docs/robots.txt``
* ``llms.txt``     — concise LLM guide, copied from ``docs/llms.txt``
* ``llms-full.txt``— full guide with examples, copied from ``docs/llms-full.txt``

Run from the repository root::

    uv run python docs/build_docs.py

The web root served by nginx is ``html/coolipy/``, so ``llms.txt`` lands at
``https://<domain>/llms.txt`` exactly where LLM crawlers expect it.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
TEMPLATES_DIR = DOCS_DIR / "templates"
OUTPUT_DIR = REPO_ROOT / "html"  # pdoc nests the package below this
WEB_ROOT = OUTPUT_DIR / "coolipy"  # what nginx actually serves
SITE_URL = "https://coolipydocs.gabrielbocchini.com.br"

# The full documented module surface. Keep in sync with the README.
MODULES = [
    "coolipy",
    "coolipy.async_client",
    "coolipy.client",
    "coolipy.enums",
    "coolipy.exceptions",
    "coolipy.models.applications",
    "coolipy.models.base",
    "coolipy.models.common",
    "coolipy.models.databases",
    "coolipy.models.deployments",
    "coolipy.models.projects",
    "coolipy.models.s3_storages",
    "coolipy.models.security",
    "coolipy.models.servers",
    "coolipy.models.services",
    "coolipy.models.system",
    "coolipy.models.teams",
    "coolipy.resources.applications",
    "coolipy.resources.databases",
    "coolipy.resources.deployments",
    "coolipy.resources.projects",
    "coolipy.resources.s3_storages",
    "coolipy.resources.security",
    "coolipy.resources.servers",
    "coolipy.resources.services",
    "coolipy.resources.tags",
    "coolipy.resources.teams",
]


def build_html() -> None:
    """Generate the pdoc3 HTML using the custom template overrides."""
    cmd = [
        sys.executable,
        "-m",
        "pdoc",
        "--html",
        "--force",
        "--template-dir",
        str(TEMPLATES_DIR),
        "-o",
        str(OUTPUT_DIR),
        *MODULES,
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def write_sitemap() -> None:
    """Emit ``sitemap.xml`` from the pages that actually exist on disk."""
    pages = sorted(WEB_ROOT.rglob("*.html"))

    def url_for(path: Path) -> str:
        rel = path.relative_to(WEB_ROOT).as_posix()
        if rel == "index.html":
            return f"{SITE_URL}/"
        return f"{SITE_URL}/{rel}"

    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    entries = []
    for page in pages:
        rel = page.relative_to(WEB_ROOT).as_posix()
        priority = "1.00" if rel == "index.html" else "0.80"
        entries.append(
            "  <url>\n"
            f"    <loc>{url_for(page)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )

    body = "\n".join(entries)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        '      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9\n'
        '            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    (WEB_ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Wrote sitemap.xml ({len(pages)} pages)")


def copy_assets() -> None:
    """Copy the discovery assets that live at the site root."""
    for name in ("robots.txt", "llms.txt", "llms-full.txt"):
        src = DOCS_DIR / name
        if src.exists():
            (WEB_ROOT / name).write_bytes(src.read_bytes())
            print(f"Copied {name}")
        else:
            print(f"WARNING: missing {src}")


def main() -> None:
    build_html()
    write_sitemap()
    copy_assets()
    print(f"Docs ready in {WEB_ROOT}")


if __name__ == "__main__":
    main()
