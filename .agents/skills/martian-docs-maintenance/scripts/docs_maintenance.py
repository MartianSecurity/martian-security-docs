#!/usr/bin/env python3
"""Read-only Martian docs inventory, PNG inspection and trusted public readback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from urllib.parse import quote, unquote, urlsplit
import zlib

MAX_BYTES = 80 * 1024 * 1024
REQUIREMENT_FIELDS = ("numberedTaskStages", "requiredValidation", "screenshotIds")
PNG_METADATA = {"tEXt", "zTXt", "iTXt", "eXIf"}


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=30
    )
    if result.returncode:
        raise ValueError(f"Git read failed: {args[0]}")
    return result.stdout.strip()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def contained(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("A relative path escapes the expected directory")
    value = (root / rel).resolve()
    if not value.is_relative_to(root.resolve()):
        raise ValueError("A symlink escapes the expected directory")
    return value


def compare_baseline(old_coverage, coverage, old_captures, captures):
    """Report review-needed contract changes; added guides/captures are allowed."""
    current = {row["id"]: row for row in coverage["guides"]}
    changes = []
    for before in old_coverage["guides"]:
        after = current.get(before["id"])
        if after is None:
            changes.append({"guide": before["id"], "change": "guide_removed"})
            continue
        for field in REQUIREMENT_FIELDS:
            if before.get(field) != after.get(field):
                changes.append({"guide": before["id"], "change": field})
        if not set(before.get("screenshots", [])) <= set(after.get("screenshots", [])):
            changes.append({"guide": before["id"], "change": "screenshot_requirement_removed"})
    current_images = {row["id"]: row for row in captures["screenshots"]}
    for before in old_captures["screenshots"]:
        if current_images.get(before["id"]) != before:
            changes.append({"capture": before["id"], "change": "changed_or_removed"})
    return changes


def audit(repo: Path, baseline: str | None = None):
    repo = repo.resolve(strict=True)
    coverage = read_json(repo / "quality/coverage.json")
    captures = read_json(repo / "quality/screenshots.json")
    guides, images = coverage["guides"], captures["screenshots"]
    issues = []
    for kind, rows in (("guide", guides), ("capture", images)):
        ids = [row["id"] for row in rows]
        if len(ids) != len(set(ids)):
            issues.append({"kind": kind, "issue": "duplicate_id"})
    for row in images:
        try:
            image = contained(repo / "public/media/screenshots", row["file"])
            if not image.is_file():
                issues.append({"capture": row["id"], "issue": "missing_file"})
            elif sha256(image) != row.get("sha256"):
                issues.append({"capture": row["id"], "issue": "hash_mismatch"})
        except ValueError:
            issues.append({"capture": row["id"], "issue": "unsafe_file_path"})
    report = {
        "repo": str(repo),
        "head": git(repo, "rev-parse", "HEAD"),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "dirtyEntries": len(git(repo, "status", "--porcelain=v1").splitlines()),
        "guides": len(guides),
        "qualificationCounts": {
            state: sum(row.get("qualification") == state for row in guides)
            for state in sorted({str(row.get("qualification")) for row in guides})
        },
        "incompleteGuides": [row["id"] for row in guides if row.get("qualification") != "verified"],
        "captureReferences": len(images),
        "uniqueCaptureFiles": len({row["file"] for row in images}),
        "captureIssues": issues,
        "baselineChangesRequiringReview": [],
        "scope": "Inventory and capture hashes only; run the owning repository checks separately.",
    }
    if baseline:
        old_coverage = json.loads(git(repo, "show", f"{baseline}:quality/coverage.json"))
        old_captures = json.loads(git(repo, "show", f"{baseline}:quality/screenshots.json"))
        report["baselineRef"] = baseline
        report["baselineChangesRequiringReview"] = compare_baseline(
            old_coverage, coverage, old_captures, captures
        )
    return report


def inspect_png(path: Path):
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("PNG exceeds the inspection byte bound")
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Not a PNG file")
    position, chunks, size = 8, [], None
    while position < len(raw):
        if position + 12 > len(raw):
            raise ValueError("Truncated PNG chunk")
        length = struct.unpack(">I", raw[position : position + 4])[0]
        end = position + 12 + length
        if end > len(raw):
            raise ValueError("Truncated PNG payload")
        kind = raw[position + 4 : position + 8]
        data = raw[position + 8 : end - 4]
        checksum = struct.unpack(">I", raw[end - 4 : end])[0]
        if zlib.crc32(kind + data) & 0xFFFFFFFF != checksum:
            raise ValueError("PNG CRC mismatch")
        name = kind.decode("ascii")
        if not chunks:
            if name != "IHDR" or length != 13:
                raise ValueError("PNG is missing its initial IHDR")
            size = struct.unpack(">II", data[:8])
        elif name == "IHDR":
            raise ValueError("Duplicate PNG IHDR")
        chunks.append(name)
        position = end
        if name == "IEND":
            if length or position != len(raw):
                raise ValueError("PNG has invalid IEND or trailing bytes")
            break
    if not chunks or chunks[-1] != "IEND" or "IDAT" not in chunks or not all(size or ()):
        raise ValueError("PNG is incomplete")
    metadata = sorted(set(chunks) & PNG_METADATA)
    return {
        "file": str(path), "bytes": len(raw), "width": size[0], "height": size[1],
        "sha256": hashlib.sha256(raw).hexdigest(), "crcPassed": True,
        "metadataChunksNeedingReview": metadata,
        "matchesCurrentCaptureViewport": size == (1440, 1000),
        "scope": "Byte inspection only; view/decode the image and review authenticity, readability and secrets.",
    }


def public_route(path: str) -> str:
    parts = urlsplit(path)
    decoded = unquote(parts.path)
    if (parts.scheme or parts.netloc or parts.query or parts.fragment
            or not decoded.startswith("/") or decoded.startswith("//")
            or "\\" in decoded or "\0" in decoded
            or any(part in {".", ".."} for part in decoded.split("/"))):
        raise ValueError("Use a site-relative route without queries, fragments or traversal")
    return decoded


def https_site(site: str) -> str:
    parts = urlsplit(site)
    if (parts.scheme != "https" or not parts.hostname or parts.username or parts.password
            or parts.query or parts.fragment or any(ord(c) < 33 for c in site)):
        raise ValueError("Use a public HTTPS site without credentials, query or fragment")
    if any(part in {".", ".."} for part in unquote(parts.path).split("/")):
        raise ValueError("Site base contains traversal")
    return site.rstrip("/")


def expected_file(root: Path, route: str) -> Path:
    relative = route.lstrip("/")
    if route.endswith("/"):
        relative += "index.html"
    return contained(root, relative)


def fetch_https(url: str, target: Path, timeout: int):
    result = subprocess.run(
        ["curl", "--disable", "--silent", "--show-error", "--fail", "--location", "--max-redirs", "3",
         "--proto", "=https", "--proto-redir", "=https", "--max-time", str(timeout),
         "--max-filesize", str(MAX_BYTES), "--output", str(target),
         "--write-out", "%{http_code}\n%{ssl_verify_result}\n%{url_effective}", url],
        capture_output=True, text=True, timeout=timeout + 5,
    )
    if result.returncode:
        raise ValueError(f"Trusted HTTPS GET failed (curl exit {result.returncode})")
    values = result.stdout.splitlines()
    if len(values) != 3 or values[0] != "200" or values[1] != "0":
        raise ValueError("Response is not HTTP 200 with verified TLS")
    effective = https_site(values[2])
    if target.stat().st_size > MAX_BYTES:
        raise ValueError("Response exceeds the byte bound")
    return effective


def verify_published(repo: Path, site: str, paths: list[str], expected_root: Path | None, timeout: int):
    base = https_site(site)
    root = (expected_root or repo / "dist").resolve(strict=True)
    results = []
    for supplied in paths:
        route = public_route(supplied)
        expected = expected_file(root, route)
        if not expected.is_file():
            raise ValueError(f"Expected artifact missing for route: {route}")
        with tempfile.TemporaryDirectory(prefix="martian-docs-readback-") as temp:
            target = Path(temp) / "body"
            effective = fetch_https(base + quote(route, safe="/-._~"), target, timeout)
            actual_hash, wanted_hash = sha256(target), sha256(expected)
            results.append({
                "path": route, "effectiveUrl": effective, "status": 200, "tlsVerified": True,
                "bytes": target.stat().st_size, "sha256": actual_hash,
                "matchesExpectedArtifact": actual_hash == wanted_hash,
            })
    return {
        "site": base, "expectedRoot": str(root), "checks": results,
        "allHashesMatch": all(row["matchesExpectedArtifact"] for row in results),
        "scope": "Public byte readback only; does not prove CI, browser usability or product behavior.",
    }


def emit(value, output: Path | None):
    content = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if output:
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
    print(content, end="")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inventory = sub.add_parser("audit", help="Read current coverage, capture hashes and optional baseline changes")
    inventory.add_argument("--repo", type=Path, required=True)
    inventory.add_argument("--baseline-ref")
    png = sub.add_parser("inspect-png", help="Inspect PNG bytes, not visual/privacy correctness")
    png.add_argument("file", type=Path)
    published = sub.add_parser("verify-published", help="Compare explicit artifacts with trusted HTTPS GETs")
    published.add_argument("--repo", type=Path, required=True)
    published.add_argument("--site", required=True)
    published.add_argument("--path", action="append", required=True, dest="paths")
    published.add_argument("--expected-root", type=Path)
    published.add_argument("--timeout", type=int, default=30)
    for item in (inventory, png, published):
        item.add_argument("--json-out", type=Path, help="Exclusively create a private JSON report; never overwrite")
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            report = audit(args.repo, args.baseline_ref)
            failed = bool(report["captureIssues"] or report["baselineChangesRequiringReview"])
        elif args.command == "inspect-png":
            report = inspect_png(args.file)
            failed = bool(report["metadataChunksNeedingReview"] or not report["matchesCurrentCaptureViewport"])
        else:
            if not 1 <= args.timeout <= 120:
                raise ValueError("Timeout must be between 1 and 120 seconds")
            report = verify_published(args.repo, args.site, args.paths, args.expected_root, args.timeout)
            failed = not report["allHashesMatch"]
        emit(report, args.json_out)
        return 1 if failed else 0
    except (OSError, ValueError, KeyError, TypeError, struct.error, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
