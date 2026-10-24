"""Build a web view of the public vault without modifying canonical notes."""
from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / ".site-docs"
WIKI = re.compile(r"\[\[([^\]]+)\]\]")
HUB_TITLES = {
    "Topic Hub": "주제별 찾아보기",
    "Organization Hub": "기관과 역할",
    "Country Hub": "국가별 자료",
    "Timeline Hub": "일정별 자료",
}
EVIDENCE = {
    "Confirmed": "공식 원문 확인",
    "Supported": "복수 근거 확인",
    "Reported": "발표 자료 기반",
    "Inferred": "근거에 기반한 해석",
    "Unverified": "추가 확인 필요",
}


def read_note(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path.name}")
    return yaml.safe_load(match[1]), match[2].lstrip()


def target_path(path: Path) -> str:
    if path.name == "HOME.md":
        return "index.md"
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return f"{path.parent.name}/{slug}.md"


def relative_link(current: str, destination: str) -> str:
    return posixpath.relpath(destination, posixpath.dirname(current) or ".")


def dump_page(path: str, meta: dict, body: str) -> None:
    out = DOCS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    out.write_text(f"---\n{frontmatter}---\n\n{body.rstrip()}\n", encoding="utf-8")


def main() -> None:
    # This is a fixed generated directory inside this repository, never a caller path.
    if DOCS.exists():
        if DOCS.is_symlink() or DOCS.resolve() != ROOT / ".site-docs":
            raise ValueError("Unexpected generated directory target")
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    paths = [ROOT / "HOME.md", *sorted((ROOT / "content").glob("*.md")), *sorted((ROOT / "hubs").glob("*.md"))]
    notes = {p: read_note(p) for p in paths}
    references: dict[str, Path] = {}
    ids: dict[str, Path] = {}
    for path, (meta, _) in notes.items():
        ids[meta["id"]] = path
        for key in (path.stem, meta["title"], meta["id"], *meta.get("aliases", [])):
            if key in references and references[key] != path:
                raise ValueError(f"Ambiguous note reference: {key}")
            references[key] = path

    registry = yaml.safe_load((ROOT / "data/source-registry.yaml").read_text(encoding="utf-8"))["sources"]
    sources = {s["id"]: s for s in registry}
    claims = json.loads((ROOT / "data/claims.json").read_text(encoding="utf-8"))["claims"]

    for path, (meta, body) in notes.items():
        if path.name == "HOME.md":
            continue
        current = target_path(path)
        title = HUB_TITLES.get(path.stem, meta["title"])

        def replace_wiki(match: re.Match) -> str:
            target, sep, display = match[1].partition("|")
            name, marker, anchor = target.partition("#")
            target_note = references.get(name.strip())
            if target_note is None:
                raise ValueError(f"Unknown Wikilink in {path.name}: {name}")
            label = display if sep else HUB_TITLES.get(target_note.stem, notes[target_note][0]["title"])
            href = relative_link(current, target_path(target_note))
            if marker:
                href += "#" + anchor
            return f"[{label}]({href})"

        body = WIKI.sub(replace_wiki, body)
        if path.stem in HUB_TITLES:
            body = re.sub(r"^# .*$", "# " + title, body, count=1, flags=re.M)
            body = body.replace("## Notes", "## 문서 목록")
        for sid in meta.get("source_ids", []):
            if sid not in sources:
                raise ValueError(f"Unknown source: {sid}")
            href = relative_link(current, "sources.md") + "#" + sid.lower()
            body = body.replace(f"`{sid}`", f"[{sid}]({href})")
        document_meta = [f'<span class="kb-evidence">{html.escape(EVIDENCE[meta["evidence_level"]])}</span>']
        if meta.get("last_verified"):
            document_meta.append(f'<span>확인일 {meta["last_verified"]}</span>')
        if any(sources[sid].get("status") == "consultation-draft" for sid in meta.get("source_ids", [])):
            document_meta.append("<span>KSGA 자료: 공개회람본 기준</span>")
        metadata_html = '<div class="kb-document-meta">' + "".join(document_meta) + "</div>\n"
        body = re.sub(r"(^# [^\n]+\n)", lambda m: m[1] + "\n" + metadata_html, body, count=1, flags=re.M)
        if meta.get("source_ids"):
            body += '\n\n<div class="kb-sources" markdown="1">\n\n## 공식 출처\n\n'
            for sid in meta["source_ids"]:
                source = sources[sid]
                body += f'- [{source["title"]}]({source["url"]}) · {source["version"]}\n'
            body += "\n</div>\n"
        related = [ids[x] for x in meta.get("related", [])]
        if related:
            body += "\n## 함께 읽기\n\n"
            for target in related:
                label = HUB_TITLES.get(target.stem, notes[target][0]["title"])
                body += f"- [{label}]({relative_link(current, target_path(target))})\n"
        dump_page(current, {"title": title, "description": title + "의 원문 근거와 한국어 해설"}, body)

    home = (ROOT / "web/home.md").read_text(encoding="utf-8")
    for key, value in {"note_count": len(notes), "source_count": len(sources), "claim_count": len(claims)}.items():
        home = home.replace("{{" + key + "}}", str(value))
    (DOCS / "index.md").write_text(home, encoding="utf-8")
    source_body = "# 공식 출처\n\n발행기관과 판본, 확인일을 함께 기록합니다. 원문은 공식 링크에서 확인할 수 있습니다.\n\n"
    for source in registry:
        sid = source["id"]
        source_body += f'## {sid} {{#{sid.lower()}}}\n\n### {source["title"]}\n\n'
        source_body += f'- **발행기관:** {source["organization"]}\n- **판본:** {source["version"]}\n'
        if source.get("publication_date"):
            source_body += f'- **공개·발행일:** {source["publication_date"]}\n'
        if source.get("effective_date"):
            source_body += f'- **시행일:** {source["effective_date"]}\n'
        if source.get("consultation_end"):
            source_body += f'- **상태:** 공개회람 · 의견수렴 {source["consultation_start"]}–{source["consultation_end"]}\n'
        source_body += f'- **확인일:** {source["last_verified"]}\n- **근거 위치:** {source["source_locator"]}\n\n[공식 원문과 공지 열기]({source["url"]})\n\n'
    dump_page("sources.md", {"title": "공식 출처"}, source_body)
    claim_body = "# 핵심 주장과 근거\n\n핵심 수치와 표준 상태를 원문의 조항까지 확인할 수 있도록 연결했습니다.\n\n"
    for claim in claims:
        sid = claim["source_id"]
        claim_body += f'## {claim["claim_id"]}\n\n{claim["claim"]}\n\n'
        claim_body += f'[{sources[sid]["title"]}](sources.md#{sid.lower()}) · {claim["source_locator"]}\n\n'
        claim_body += f'확인일: {claim["verified_at"]}\n\n'
    dump_page("claims.md", {"title": "핵심 주장과 근거"}, claim_body)
    shutil.copytree(ROOT / "web/assets", DOCS / "assets")
    manifest = {"notes": len(notes), "sources": len(sources), "claims": len(claims), "pages": [target_path(p) for p in paths] + ["sources.md", "claims.md"]}
    (ROOT / ".site-build.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f'Prepared {len(notes)} vault notes + 2 evidence pages; {len(sources)} sources; {len(claims)} claims')


if __name__ == "__main__":
    main()
