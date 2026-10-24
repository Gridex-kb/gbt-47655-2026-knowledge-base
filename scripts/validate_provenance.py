#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) or {}


def main(root: Path) -> int:
    errors: list[str] = []
    registry = yaml.safe_load((root / "data/source-registry.yaml").read_text(encoding="utf-8"))
    source_ids = {item["id"] for item in registry.get("sources", [])}
    if len(source_ids) != len(registry.get("sources", [])):
        errors.append("duplicate source id")

    note_files = [root / "HOME.md"]
    note_files += list((root / "content").glob("*.md"))
    note_files += list((root / "hubs").glob("*.md"))
    document_ids: set[str] = set()
    for path in note_files:
        fm = load_frontmatter(path)
        for key in ("id", "title", "type", "status", "evidence_level", "source_ids", "last_verified", "aliases", "tags", "related"):
            if key not in fm:
                errors.append(f"{path.name}: missing {key}")
        doc_id = fm.get("id")
        if doc_id in document_ids:
            errors.append(f"duplicate document id: {doc_id}")
        document_ids.add(doc_id)
        for source_id in fm.get("source_ids") or []:
            if source_id not in source_ids:
                errors.append(f"{path.name}: unknown source id {source_id}")

    claims = json.loads((root / "data/claims.json").read_text(encoding="utf-8"))
    claim_ids: set[str] = set()
    for claim in claims.get("claims", []):
        claim_id = claim["claim_id"]
        if claim_id in claim_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if claim["source_id"] not in source_ids:
            errors.append(f"{claim_id}: unknown source id {claim['source_id']}")
        if not claim.get("source_locator"):
            errors.append(f"{claim_id}: missing source locator")

    public_text = "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*") if p.is_file() and p.suffix in {".md", ".yaml", ".json"})
    for forbidden in ("GBT-47655-2026.pdf", "knowledge-base-dev/sources"):
        if forbidden in public_text:
            errors.append(f"public repository exposes private artifact reference: {forbidden}")

    if errors:
        print("Provenance validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Provenance validation OK: {len(note_files)} notes, {len(source_ids)} sources, {len(claim_ids)} claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()))
