#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

REQUIRED = {"title", "type", "status", "evidence_level"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def frontmatter(text: str):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    keys = set()
    for line in text[4:end].splitlines():
        if line and not line.startswith(" ") and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def knowledge_notes(root: Path):
    notes = []
    home = root / "HOME.md"
    if home.exists():
        notes.append(home)
    for folder in ("content", "hubs"):
        path = root / folder
        if path.exists():
            notes.extend(path.rglob("*.md"))
    return notes


def main(root: Path) -> int:
    notes = knowledge_notes(root)
    stems = {p.stem for p in notes}
    errors = []
    for private_path in ("sources", "project", "gcp", "data/source-archive.yaml", "data/source-candidates.json"):
        if (root / private_path).exists():
            errors.append(f"{private_path}: belongs in the private <name>-dev repository")
    seen_ids = {}
    id_re = re.compile(r"^id:\s*[\"']?([^\"'\n]+)", re.M)
    for p in notes:
        text = p.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{p}: missing YAML frontmatter")
        else:
            missing = REQUIRED - fm
            if missing:
                errors.append(f"{p}: missing frontmatter fields {sorted(missing)}")
        match = id_re.search(text[:1500])
        if match:
            doc_id = match.group(1).strip()
            if doc_id in seen_ids:
                errors.append(f"duplicate id {doc_id}: {seen_ids[doc_id]} and {p}")
            seen_ids[doc_id] = p
        for target in WIKILINK.findall(text):
            target = target.strip()
            if target and target not in stems:
                errors.append(f"{p}: broken wikilink [[{target}]]")
    if errors:
        print("Knowledge Base validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Knowledge Base validation OK: {len(notes)} knowledge notes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()))
