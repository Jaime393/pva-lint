#!/usr/bin/env python3
"""Offline artifact-readiness inventory, not scientific or public-access validation."""
import argparse
import hashlib
import json
from pathlib import Path
import re

MAX_TEXT_BYTES = 2 * 1024 * 1024


def regular(path):
    return path.is_file() and not path.is_symlink()


def evidence(path, root):
    size = path.stat().st_size
    return {"path": path.relative_to(root).as_posix(), "bytes": size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if size <= MAX_TEXT_BYTES else None,
            "read_state": "full" if size <= MAX_TEXT_BYTES else "not_read_size_limit"}


def scan_repo(path="."):
    root = Path(path).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("repository path must be a directory")
    text_files = sorted(p for p in root.iterdir() if regular(p)
                        and p.suffix.lower() in {".md", ".tex"} and p.stat().st_size <= MAX_TEXT_BYTES)
    dois = set()
    for source in text_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        dois.update(value.rstrip(".,;:)]}>") for value in re.findall(r"10\.\d{4,}/[^\s\"<>]+", text))
    data = [p for p in root.glob("*.csv") if regular(p) and p.stat().st_size > 0]
    directory = root / "data"
    if directory.is_dir() and not directory.is_symlink():
        data += [p for p in directory.iterdir() if regular(p) and p.stat().st_size > 0]
    code = [p for p in root.iterdir() if regular(p) and p.suffix.lower() in {".py", ".js", ".ts", ".rs", ".lean", ".jl"}]
    containers = [p for p in (root / "Dockerfile", root / "docker-compose.yml") if regular(p)]
    make = root / "Makefile"
    reproduce = regular(make) and make.stat().st_size <= MAX_TEXT_BYTES and bool(
        re.search(r"^reproduce[ \t]*:(?!=)", make.read_text(encoding="utf-8", errors="replace"), re.M))
    figures = [p for p in root.iterdir() if regular(p) and p.suffix == ".py"
               and (p.name.startswith("fig") or p.name.startswith("plot"))]
    groups = {"doi": text_files if dois else [], "datos": data, "codigo": code,
              "docker": containers, "reproduce": [make] if reproduce else [], "figuras": figures}
    checks = {name: {"state": "observed" if sources else "missing",
                     "evidence": [evidence(p, root) for p in sorted(set(sources))]}
              for name, sources in groups.items()}
    checks["doi"]["identifiers"] = sorted(dois)
    checks["doi"]["resolution_checked"] = False
    observed = sum(item["state"] == "observed" for item in checks.values())
    return {
        "schema": "pva.artifact-readiness/v1",
        "checks": checks,
        "observed_checks": observed,
        "total_checks": len(checks),
        "structural_score": round(observed / len(checks), 3),
        "carencias": [name for name, item in checks.items() if item["state"] == "missing"],
        "public_access_verified": False,
        "reproduction_executed": False,
        "scientific_claims_validated": False,
        "network_used": False,
        "scope": "File presence and declared reproduce target only; no DOI resolution, license/publicity proof, container build, reproduction or scientific certification.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = scan_repo(args.path)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Blocked: {error}\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Artifact presence: {report['observed_checks']}/{report['total_checks']}")
        for name, check in report["checks"].items():
            print(f"  {name}: {check['state']}")
        print(report["scope"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
