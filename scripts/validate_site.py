"""Validate rendered links and the public-only deployment boundary."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "/gbt-47655-2026-knowledge-base/"


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if fields.get("id"):
            self.ids.add(fields["id"])
        if tag in {"a", "link", "script", "img"}:
            for attr in ("href", "src"):
                if fields.get(attr):
                    self.links.append(fields[attr])


def main(site: Path) -> int:
    site = site.resolve()
    errors: set[str] = set()
    pages = {p: Page(p.read_text(encoding="utf-8")) for p in site.rglob("*.html")}
    if not pages:
        raise ValueError("No generated HTML pages")
    manifest = json.loads((ROOT / ".site-build.json").read_text(encoding="utf-8"))
    for source in manifest["pages"]:
        target = site / ("index.html" if source == "index.md" else source[:-3] + "/index.html")
        if not target.exists():
            errors.add(f"Missing page: {source}")
    for file, page in pages.items():
        text = file.read_text(encoding="utf-8")
        if re.search(r"\[\[[^\]]+\]\]", text):
            errors.add(f"Unconverted Wikilink: {file.relative_to(site)}")
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            if path.startswith(BASE):
                target = site / path[len(BASE):]
            elif path.startswith("/"):
                errors.add(f"Link escapes project prefix: {href}")
                continue
            elif path:
                target = file.parent / path
            else:
                target = file
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(site) or not target.exists():
                errors.add(f"Broken local link: {file.relative_to(site)} → {href}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.add(f"Missing anchor: {file.relative_to(site)} → {href}")
    for file in site.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() in {".pdf", ".docx", ".txt", ".yaml", ".yml"}:
            errors.add(f"Unexpected original/config artifact: {file.relative_to(site)}")
        if file.suffix in {".html", ".json"}:
            text = file.read_text(encoding="utf-8")
            for forbidden in ("knowledge-base-dev", "source-archive.yaml", "카카오톡 받은 파일", "C:\\Users\\", "file:///"):
                if forbidden in text:
                    errors.add(f"Non-public path in artifact: {file.relative_to(site)}")
    index_file = site / "search/search_index.json"
    if not index_file.exists():
        errors.add("Missing search index")
    else:
        index = json.loads(index_file.read_text(encoding="utf-8"))
        if "관성" not in json.dumps(index, ensure_ascii=False) or "KSGA" not in json.dumps(index, ensure_ascii=False):
            errors.add("Search index lacks expected Korean/comparison content")
    if errors:
        print("Site validation FAILED")
        for message in sorted(errors):
            print("- " + message)
        return 1
    print(f'Site validation OK: {len(pages)} HTML files, all expected pages/links/anchors, Korean search, public-only artifacts')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".site-dist"))
