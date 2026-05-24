#!/usr/bin/env python3
"""Coupling audit (DL adapter): src/ <-> docs/field/module_contracts/.

Implements the DL specialization of kernel/coupling_principle.md.
Run from the project root.

Usage:
    python domains/deep_learning/audit_coupling.py
        Check coupling, write conflicts to docs/conflicts/, exit 1 if drift.

    python domains/deep_learning/audit_coupling.py --update
        Update audit_hash and last_audited in all docs to match current src.
        Use after manually confirming each doc reflects current code.

    python domains/deep_learning/audit_coupling.py --no-conflicts
        Check only; do not write any conflict files. Useful in CI for a
        clean printout.

    python domains/deep_learning/audit_coupling.py --strict
        Treat missing front-matter and missing covers as hard failures
        (default: warn).

Exit codes:
    0  clean
    1  drift detected
    2  configuration error (no src/ found, etc.)
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "src"
CONTRACTS = ROOT / "docs" / "field" / "module_contracts"
CONFLICTS = ROOT / "docs" / "conflicts"
EXEMPT_FILE = Path(__file__).resolve().parent / "coupling_exempt.txt"
REMOVED = CONTRACTS / "_removed"

SHORT_HASH_LEN = 7

# Front-matter detection: a YAML block at the very top delimited by ---.
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


# -------------------- helpers --------------------


def short_hash(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:SHORT_HASH_LEN]


def parse_front_matter(text: str) -> dict:
    """Minimal YAML parser for the front-matter schema used here.

    Supports:
        key: value
        key:
          - item1
          - item2
    """
    m = FM_RE.match(text)
    if not m:
        return {}
    body = m.group(1)
    result: dict = {}
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            result[key] = value
            i += 1
            continue
        # value on following indented lines
        items: list[str] = []
        i += 1
        while i < len(lines):
            nxt = lines[i]
            stripped_nxt = nxt.strip()
            if (
                nxt.startswith("  -")
                or nxt.startswith("- ")
                or nxt.startswith("-\t")
            ):
                items.append(nxt.lstrip(" \t-").strip())
                i += 1
            elif not stripped_nxt:
                i += 1
            else:
                break
        result[key] = items
    return result


def load_exempt() -> set[str]:
    builtin = set()  # defaults handled separately
    if not EXEMPT_FILE.exists():
        return builtin
    out = set(builtin)
    for raw in EXEMPT_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.add(line.replace("\\", "/"))
    return out


def is_default_exempt(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    return name == "__init__.py" or name.startswith("_")


def mirror_doc_for_src(src_file: Path) -> Path:
    rel = src_file.relative_to(SRC).with_suffix(".md")
    return CONTRACTS / rel


def mirror_src_for_doc(doc_file: Path) -> Path:
    rel = doc_file.relative_to(CONTRACTS).with_suffix(".py")
    return SRC / rel


def rel_to_root(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def sanitize_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")


# -------------------- issue model --------------------


@dataclass
class Issue:
    type: str
    target_artifact: str
    target_doc: str
    what: str
    resolve: str
    name: str  # short slug used in filename

    def fmt(self) -> str:
        return f"  [{self.type}] {self.target_artifact or '-'}  ::  {self.target_doc or '-'}"


# -------------------- conflict writing --------------------


def write_conflict(issue: Issue) -> Optional[Path]:
    CONFLICTS.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    fn = CONFLICTS / f"{today}_{sanitize_name(issue.name)}.md"
    if fn.exists():
        return None  # do not overwrite existing
    fn.write_text(
        f"""---
type: {issue.type}
discovered: {today}
discovered_by: audit_coupling.py
target_artifact: {issue.target_artifact}
target_doc: {issue.target_doc}
status: open
---

# Conflict: {issue.name}

## What conflicts

{issue.what}

## Why it matters

Drift between artifacts and docs accumulates silently. This conflict must be
resolved before subsequent locate / reflux actions are considered complete.

## Resolve by

{issue.resolve}

## Resolution (filled when resolved)

- date:
- action taken:
- by:
- related commit / run:
""",
        encoding="utf-8",
    )
    return fn


# -------------------- audit_hash updating --------------------


def update_audit_hash(doc_file: Path, new_hash: str) -> None:
    text = doc_file.read_text(encoding="utf-8")
    today = date.today().isoformat()
    has_hash = re.search(r"^audit_hash:.*$", text, flags=re.MULTILINE)
    has_audited = re.search(r"^last_audited:.*$", text, flags=re.MULTILINE)

    if has_hash:
        text = re.sub(
            r"^(audit_hash:\s*).+$",
            f"\\g<1>{new_hash}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    if has_audited:
        text = re.sub(
            r"^(last_audited:\s*).+$",
            f"\\g<1>{today}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    if not has_hash or not has_audited:
        # Insert missing fields just before the closing ---.
        m = FM_RE.match(text)
        if m:
            inner = m.group(1)
            inserts = []
            if not has_audited:
                inserts.append(f"last_audited: {today}")
            if not has_hash:
                inserts.append(f"audit_hash: {new_hash}")
            new_inner = inner.rstrip() + "\n" + "\n".join(inserts)
            text = "---\n" + new_inner + "\n---\n" + text[m.end():]

    doc_file.write_text(text, encoding="utf-8")


# -------------------- audit --------------------


def audit(update: bool, write_conflicts_flag: bool, strict: bool) -> int:
    if not SRC.exists():
        print(f"[audit_coupling] {rel_to_root(SRC)} does not exist yet.")
        print("[audit_coupling] nothing to audit. exit 0.")
        return 0

    CONTRACTS.mkdir(parents=True, exist_ok=True)

    issues: list[Issue] = []
    exempt = load_exempt()

    # ---- 1. src files require mirror docs ----
    for src_file in sorted(SRC.rglob("*.py")):
        rel = rel_to_root(src_file)
        if is_default_exempt(rel) or rel in exempt:
            continue
        doc = mirror_doc_for_src(src_file)
        if not doc.exists():
            issues.append(
                Issue(
                    type="uncovered-artifact",
                    target_artifact=rel,
                    target_doc=rel_to_root(doc),
                    what=f"{rel} exists but has no mirror doc at {rel_to_root(doc)}.",
                    resolve=(
                        "Create the mirror doc using "
                        "domains/deep_learning/templates/module_contract.md, "
                        "or add the path to domains/deep_learning/coupling_exempt.txt."
                    ),
                    name=f"{src_file.stem}_uncovered",
                )
            )

    # ---- 2. docs require valid front-matter + mirror src + audit_hash ----
    if CONTRACTS.exists():
        for doc_file in sorted(CONTRACTS.rglob("*.md")):
            # skip _removed/, README.md, and any file under templates/
            rel_doc = rel_to_root(doc_file)
            if "/_removed/" in rel_doc or "_removed" in doc_file.parts:
                continue
            if doc_file.name.lower() == "readme.md":
                continue
            if rel_doc in exempt:
                continue

            text = doc_file.read_text(encoding="utf-8")
            fm = parse_front_matter(text)

            if not fm:
                issues.append(
                    Issue(
                        type="no-front-matter",
                        target_artifact="",
                        target_doc=rel_doc,
                        what=f"{rel_doc} has no front-matter; cannot audit coupling.",
                        resolve=(
                            "Add front-matter using "
                            "domains/deep_learning/templates/module_contract.md."
                        ),
                        name=f"{doc_file.stem}_no_frontmatter",
                    )
                )
                continue

            covers = fm.get("covers", [])
            if isinstance(covers, str):
                covers = [covers]
            covers = [c.replace("\\", "/").strip() for c in covers if c.strip()]

            if not covers:
                if strict:
                    issues.append(
                        Issue(
                            type="no-covers",
                            target_artifact="",
                            target_doc=rel_doc,
                            what=f"{rel_doc} front-matter has no 'covers' field.",
                            resolve="Add a covers: list pointing to the src file(s) this doc describes.",
                            name=f"{doc_file.stem}_no_covers",
                        )
                    )
                continue

            # validate each covers entry
            first_existing: Optional[Path] = None
            for c in covers:
                cp = ROOT / c
                if not cp.exists():
                    issues.append(
                        Issue(
                            type="orphan-doc",
                            target_artifact=c,
                            target_doc=rel_doc,
                            what=f"{rel_doc} declares covers: {c}, but that file does not exist.",
                            resolve=(
                                "Either remove this doc (move to docs/field/module_contracts/_removed/), "
                                "update 'covers' to point to the right path, or restore the src file."
                            ),
                            name=f"{doc_file.stem}_orphan",
                        )
                    )
                elif first_existing is None:
                    first_existing = cp

            if first_existing is None:
                continue

            # ---- audit_hash drift check ----
            current = short_hash(first_existing)
            recorded = str(fm.get("audit_hash", "")).strip()

            if update:
                if recorded != current:
                    update_audit_hash(doc_file, current)
                continue

            if not recorded:
                if strict:
                    issues.append(
                        Issue(
                            type="no-audit-hash",
                            target_artifact=rel_to_root(first_existing),
                            target_doc=rel_doc,
                            what=f"{rel_doc} has no audit_hash. Code drift cannot be detected.",
                            resolve="Run 'python domains/deep_learning/audit_coupling.py --update' to initialize.",
                            name=f"{doc_file.stem}_no_hash",
                        )
                    )
                continue

            if recorded != current:
                issues.append(
                    Issue(
                        type="artifact-vs-doc",
                        target_artifact=rel_to_root(first_existing),
                        target_doc=rel_doc,
                        what=(
                            f"{rel_to_root(first_existing)} hash changed: "
                            f"recorded {recorded} -> current {current}. "
                            f"Doc may be stale."
                        ),
                        resolve=(
                            "Review the code change. If semantics did not change, "
                            "run 'python domains/deep_learning/audit_coupling.py --update'. "
                            "If semantics changed, update the doc first, then --update."
                        ),
                        name=f"{doc_file.stem}_drift",
                    )
                )

            # ---- verified_by must exist ----
            verified_by = fm.get("verified_by", [])
            if isinstance(verified_by, str):
                verified_by = [verified_by]
            for v in verified_by:
                v = v.replace("\\", "/").strip()
                if not v:
                    continue
                vp = ROOT / v
                if not vp.exists():
                    issues.append(
                        Issue(
                            type="missing-verifier",
                            target_artifact=v,
                            target_doc=rel_doc,
                            what=f"{rel_doc} declares verified_by: {v}, but that file does not exist.",
                            resolve="Create the test/probe file, or remove the claim from front-matter.",
                            name=f"{doc_file.stem}_test_missing_{Path(v).stem}",
                        )
                    )

    # ---- report ----
    if not issues:
        print("[audit_coupling] clean.")
        return 0

    print(f"[audit_coupling] {len(issues)} issue(s):")
    for issue in issues:
        print(issue.fmt())

    if write_conflicts_flag:
        written = 0
        for issue in issues:
            if write_conflict(issue) is not None:
                written += 1
        print(
            f"[audit_coupling] wrote {written} new conflict file(s) to "
            f"{rel_to_root(CONFLICTS)} "
            f"(existing same-name conflicts not overwritten)."
        )

    return 1


# -------------------- cli --------------------


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Audit coupling between src/ and docs/field/module_contracts/."
    )
    ap.add_argument(
        "--update",
        action="store_true",
        help="Update audit_hash and last_audited in docs to match current src.",
    )
    ap.add_argument(
        "--no-conflicts",
        action="store_true",
        help="Do not write conflict files; only print report.",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing front-matter / covers / audit_hash as hard failures.",
    )
    args = ap.parse_args()

    code = audit(
        update=args.update,
        write_conflicts_flag=not args.no_conflicts and not args.update,
        strict=args.strict,
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
