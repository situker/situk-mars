#!/usr/bin/env python3
"""Build reproducible, standalone language packs using only the standard library.

Run from any directory with Python 3.11+: ``python tools/build_packages.py``.
Archives and their SHA-256 checksums are written only to this repository's dist/.
Source files are never modified. Symlinks, Windows reparse points and Python
bytecode caches are not included. Each archive contains situk-mars/ as its root.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import zipfile


VERSION = "0.2.0"
LANGUAGES = ("en", "zh-CN")
ZIP_TIME = (2026, 10, 26, 0, 0, 0)
SKIP_DIRECTORIES = frozenset({"__pycache__", ".git", ".local", "dist"})
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def is_link_or_reparse(path: Path) -> bool:
    metadata = path.lstat()
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & REPARSE_POINT
    )


def checked_child(root: Path, relative: str) -> Path:
    """Reject redirected ancestors before resolving a repository-relative path."""
    candidate = root
    for component in Path(relative).parts:
        if component in {"", ".", ".."}:
            raise ValueError(f"Unsafe relative path: {relative}")
        candidate = candidate / component
        if candidate.exists() or candidate.is_symlink():
            if is_link_or_reparse(candidate):
                raise ValueError(f"Path must not be a symlink/reparse point: {candidate}")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise ValueError(f"Path escapes repository: {relative}")
    return candidate


def collect_files(source: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}

    def visit(directory: Path) -> None:
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            if is_link_or_reparse(path):
                continue
            if path.is_dir():
                if path.name not in SKIP_DIRECTORIES:
                    visit(path)
                continue
            if not path.is_file():
                continue
            if path.suffix.lower() in {".pyc", ".pyo"}:
                continue
            relative = path.relative_to(source).as_posix()
            if relative == "MANIFEST.sha256":
                continue  # Regenerated from the exact bytes included in the archive.
            if "\\" in relative or any(part in {"", ".", ".."} for part in relative.split("/")):
                raise ValueError(f"Unsafe archive member: {relative!r}")
            if "\n" in relative or "\r" in relative:
                raise ValueError(f"Filename cannot be represented in checksum manifest: {relative!r}")
            files[relative] = path.read_bytes()

    visit(source)
    for required in ("SKILL.md", "README.md", "LICENSE", "policy.json"):
        if required not in files:
            raise ValueError(f"Required file is missing from {source.name}: {required}")
    policy = json.loads(files["policy.json"])
    if policy.get("rule_version") != VERSION:
        raise ValueError(f"Expected rule_version {VERSION}, got {policy.get('rule_version')!r}")
    return files


def make_archive(files: dict[str, bytes]) -> bytes:
    manifest = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(files.items())
    ).encode("utf-8")
    archive_files = {**files, "MANIFEST.sha256": manifest}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(archive_files.items()):
            member = zipfile.ZipInfo(f"situk-mars/{name}", date_time=ZIP_TIME)
            member.create_system = 3
            member.external_attr = (stat.S_IFREG | 0o644) << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(member, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def write_atomic(path: Path, data: bytes) -> None:
    if path.exists() or path.is_symlink():
        if is_link_or_reparse(path) or not path.is_file():
            raise ValueError(f"Output must be a regular file: {path}")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".package-", suffix=".tmp", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build(root: Path) -> list[tuple[str, str, int]]:
    root = root.resolve(strict=True)
    artifacts: dict[str, bytes] = {}
    root_license = checked_child(root, "LICENSE").read_bytes()
    for language in LANGUAGES:
        source = checked_child(root, f"skills/{language}/situk-mars")
        if not source.is_dir():
            raise ValueError(f"Skill directory is missing: skills/{language}/situk-mars")
        files = collect_files(source)
        if files["LICENSE"] != root_license:
            raise ValueError(f"Language pack LICENSE differs from repository LICENSE: {language}")
        artifacts[f"situk-mars-v{VERSION}-{language}.zip"] = make_archive(files)

    # Validate and prepare every artifact before replacing any generated output.
    output = checked_child(root, "dist")
    output.mkdir(exist_ok=True)
    if not output.is_dir():
        raise ValueError("dist must be a directory")
    results = [
        (name, hashlib.sha256(data).hexdigest(), len(data))
        for name, data in artifacts.items()
    ]
    checksum_data = "".join(f"{digest}  {name}\n" for name, digest, _ in results).encode("utf-8")
    for name, data in artifacts.items():
        write_atomic(checked_child(root, f"dist/{name}"), data)
    write_atomic(checked_child(root, "dist/SHA256SUMS"), checksum_data)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    for name, digest, size in build(root):
        print(f"{digest}  dist/{name}  ({size} bytes)")
    print("Wrote dist/SHA256SUMS")


if __name__ == "__main__":
    main()
