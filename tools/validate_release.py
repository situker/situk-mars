"""Offline checks for the bilingual release; Python standard library only."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".local", "dist", "__pycache__"}
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> int:
    packs = {language: ROOT / "skills" / language / "situk-mars"
             for language in ("en", "zh-CN")}
    policies = {language: json.loads((path / "policy.json").read_text(encoding="utf-8"))
                for language, path in packs.items()}
    cn, en = policies["zh-CN"], policies["en"]
    # Presentation fields may differ. Every operational policy field must match.
    operational = lambda value: {k: v for k, v in value.items()
                                 if k not in {"promotion_notes", "rank_labels"}}
    check(operational(cn) == operational(en), "Operational policies differ")
    check(cn["rule_version"] == "0.2.0", "Unexpected rule version")
    check(cn["grade_points"] == {"commendation": 1, "third": 3, "second": 8,
                                 "first": 20, "honor": 50}, "Award pool drift")
    check(cn["weekly_caps"] == {"commendation": 2, "third": 2,
                                "second": 1, "first": 1}, "Weekly cap drift")
    check(set(en["rank_labels"]) == set(en["rank_order"]) | {"元帅"},
          "English rank labels incomplete")
    for relative in ("scripts/merit_engine.py", "scripts/simulate.py",
                     "scripts/render_english.py", "tests/test_merit_engine.py"):
        check((packs["en"] / relative).read_bytes() == (packs["zh-CN"] / relative).read_bytes(),
              f"Shared code differs: {relative}")
    for language, pack in packs.items():
        skill = (pack / "SKILL.md").read_text(encoding="utf-8")
        check(re.search(r"^name: situk-mars$", skill, re.M) is not None,
              f"Skill ID mismatch: {language}")
        check(json.loads((pack / "locale.json").read_text(encoding="utf-8"))["language"] == language,
              f"Wrong default language: {language}")
        check((pack / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes(),
              f"License mismatch: {language}")
        block = (pack / "_shared/constitution-block.md").read_text(encoding="utf-8").strip()
        check(block in skill, f"Governance summary mismatch: {language}")
        check(len(list((pack / "templates").glob("*.md"))) == 9,
              f"Expected nine templates: {language}")
    check({p.name for p in (packs["en"] / "templates").glob("*.md")} ==
          {p.name for p in (packs["zh-CN"] / "templates").glob("*.md")},
          "Template inventories differ")

    files = [p for p in ROOT.rglob("*") if p.is_file()
             and not set(p.relative_to(ROOT).parts) & IGNORED]
    # Do not print matched data: a failing secret scan must not leak the secret.
    private = re.compile(
        r"[A-Za-z]:[\\/](?:Projects|Users)[\\/]|"
        r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|"
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        re.I)
    for path in files:
        check(not path.is_symlink(), f"Symlink in distribution: {path.relative_to(ROOT)}")
        if path.suffix not in {".md", ".json", ".py", ".svg", ".mmd", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        check(private.search(text) is None, f"Private data pattern in: {path.relative_to(ROOT)}")
        check(("cd " + "meritops") not in text, f"Stale clone command: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            # Inline links only; external URLs, anchors and template placeholders are excluded.
            for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
                target = match.group(1).strip().split(' "', 1)[0].strip("<>")
                if not target or "://" in target or target.startswith(("#", "mailto:", "{")):
                    continue
                target = unquote(target.split("#", 1)[0])
                check((path.parent / target).exists(),
                      f"Missing local link in {path.relative_to(ROOT)}: {target}")
    for language in ("en", "zh-CN"):
        diagram = ROOT / f"docs/assets/architecture.{language}.svg"
        try:
            check(ET.parse(diagram).getroot().tag == "{http://www.w3.org/2000/svg}svg",
                  f"Not an SVG: {diagram.name}")
        except (OSError, ET.ParseError):
            ERRORS.append(f"Missing or invalid SVG: {diagram.name}")
    if ERRORS:
        print("Release validation FAILED:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print(f"Release validation PASSED: {len(files)} files; bilingual policy, code, links, licenses and privacy checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
