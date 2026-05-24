#!/usr/bin/env python3
"""Lightweight agentic structural harness. No external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


PKG = Path(__file__).resolve().parents[1]
TEMPLATES = PKG / "templates"
PULSE_TEMPLATE = """# Pulse

任务: <current real problem and success condition>
位置: <object/path being worked on>
最近: none
冲突: none
动作: <clarify | locate | reflux> 在 <frame | field | trace>
"""


CURRENT_TASK_TEMPLATE = "# Current Task\n\n## Object\n\n## Goal\n\n## Success Criteria\n\n## Worst Acceptable Outcome\n\n## Out of Scope\n"
SUCCESS_TEMPLATE = "# Success Criteria\n\n- stable objects have mirror docs\n- event instances have record folders\n- conflicts are explicit\n- accepted evidence refluxes into frame/field\n"
REFLUX_TEMPLATE = "# Reflux Journal\n\n| date | source | what changed | updated docs | verdict |\n|---|---|---|---|---|\n"


class HarnessError(SystemExit):
    """Expected user-facing harness error."""


def today() -> str:
    return date.today().isoformat()


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_slug(text: str) -> str:
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_\-\u4e00-\u9fff]+", "_", text)
    return text.strip("_") or "item"


def short_hash(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return hashlib.sha1(data).hexdigest()[:7]
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:7]


def short_text_hash(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:8]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def glob_segment_to_regex(segment: str) -> str:
    out = []
    for ch in segment:
        if ch == "*":
            out.append("[^/]*")
        elif ch == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(ch))
    return "".join(out)


def glob_match(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").strip("/")
    parts = pattern.replace("\\", "/").strip("/").split("/")
    regex = "^"
    for idx, part in enumerate(parts):
        if idx > 0 and parts[idx - 1] != "**":
            regex += "/"
        if part == "**":
            regex += "(?:[^/]+/)*"
        else:
            regex += glob_segment_to_regex(part)
    regex += "$"
    return re.match(regex, path) is not None


def load_yaml_subset(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    current_list: list[dict[str, Any]] | None = None
    current_item: dict[str, Any] | None = None
    current_sublist: str | None = None

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if "\t" in raw:
            raise HarnessError(f"{path}:{lineno}: tabs are not supported in project.yaml")
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent not in {0, 2, 4, 6}:
            raise HarnessError(f"{path}:{lineno}: unsupported indentation; use 0/2/4/6 spaces")
        stripped = line.strip()

        if indent == 0:
            current_list = None
            current_item = None
            current_sublist = None
            if stripped.endswith(":"):
                key = stripped[:-1].strip()
                out[key] = []
                current_list = out[key]
            elif ":" in stripped:
                key, value = stripped.split(":", 1)
                out[key.strip()] = parse_scalar(value)
            else:
                raise HarnessError(f"{path}:{lineno}: expected key: value")
            continue

        if indent == 2 and stripped.startswith("- ") and current_list is not None:
            current_item = {}
            current_list.append(current_item)
            current_sublist = None
            rest = stripped[2:].strip()
            if rest and ":" in rest:
                key, value = rest.split(":", 1)
                current_item[key.strip()] = parse_scalar(value)
            elif rest:
                raise HarnessError(f"{path}:{lineno}: expected list item as key: value")
            continue

        if indent == 4 and current_item is not None:
            if stripped.endswith(":"):
                key = stripped[:-1].strip()
                current_item[key] = []
                current_sublist = key
            elif ":" in stripped:
                key, value = stripped.split(":", 1)
                current_item[key.strip()] = parse_scalar(value)
                current_sublist = None
            else:
                raise HarnessError(f"{path}:{lineno}: expected key: value")
            continue

        if indent == 6 and stripped.startswith("- ") and current_item is not None and current_sublist:
            current_item[current_sublist].append(parse_scalar(stripped[2:].strip()))
            continue

        raise HarnessError(f"{path}:{lineno}: unsupported project.yaml shape")

    return out


def validate_config(data: dict[str, Any], path: Path) -> None:
    for key in ["semantic_root", "workspace_root", "pulse_path", "conflict_dir"]:
        if key in data and not isinstance(data[key], str):
            raise HarnessError(f"{path}: {key} must be a string")

    for section in ["stable_objects", "events"]:
        if section in data and not isinstance(data[section], list):
            raise HarnessError(f"{path}: {section} must be a list")

    for idx, rule in enumerate(data.get("stable_objects", []), start=1):
        for key in ["name", "artifact_glob", "mirror_pattern", "template"]:
            if not rule.get(key):
                raise HarnessError(f"{path}: stable_objects[{idx}] missing {key}")

    for idx, rule in enumerate(data.get("events", []), start=1):
        for key in ["name", "record_pattern", "template_dir"]:
            if not rule.get(key):
                raise HarnessError(f"{path}: events[{idx}] missing {key}")
        files = rule.get("required_files", [])
        if not isinstance(files, list) or not files:
            raise HarnessError(f"{path}: events[{idx}] required_files must be a non-empty list")


def config(root: Path) -> dict[str, Any]:
    path = root / ".agentic" / "project.yaml"
    if not path.exists():
        raise SystemExit(f"missing {rel(path, root)}; run init first")
    data = load_yaml_subset(path)
    data.setdefault("semantic_root", "semantic")
    data.setdefault("workspace_root", "workspace")
    data.setdefault("pulse_path", "semantic/pulse.md")
    data.setdefault("conflict_dir", "semantic/conflicts")
    data.setdefault("stable_objects", [])
    data.setdefault("events", [])
    validate_config(data, path)
    return data


def copy_templates(root: Path, force: bool) -> None:
    dst = root / ".agentic" / "templates"
    dst.mkdir(parents=True, exist_ok=True)
    for item in TEMPLATES.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists() and force:
                shutil.rmtree(target)
            if not target.exists():
                shutil.copytree(item, target)
        else:
            if force or not target.exists():
                shutil.copy2(item, target)


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    for d in [
        ".agentic",
        "semantic/frame",
        "semantic/field/mirrors",
        "semantic/field/contracts",
        "semantic/records/experiments",
        "semantic/records/agent_tasks",
        "semantic/trace/decisions",
        "semantic/trace/failures",
        "semantic/conflicts",
        "workspace/src",
        "workspace/configs",
        "workspace/scripts",
        "workspace/tests",
        "workspace/probes",
        "workspace/runs",
        "workspace/checkpoints",
    ]:
        (root / d).mkdir(parents=True, exist_ok=True)

    copy_templates(root, args.force)
    write_text(root / ".agentic/project.yaml", read_text(TEMPLATES / "project.yaml"), force=args.force)
    write_text(root / "semantic/pulse.md", PULSE_TEMPLATE, force=args.force)
    write_text(root / "semantic/frame/current_task.md", CURRENT_TASK_TEMPLATE, force=args.force)
    write_text(root / "semantic/frame/success_criteria.md", SUCCESS_TEMPLATE, force=args.force)
    write_text(root / "semantic/trace/reflux_journal.md", REFLUX_TEMPLATE, force=args.force)
    write_text(root / "semantic/conflicts/index.md", "# Conflict Index\n\nNo open conflicts yet.\n", force=args.force)
    print(f"[init] ready: {root}")
    return 0


def cmd_pulse(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    pulse = root / cfg["pulse_path"]
    if not pulse.exists():
        write_text(pulse, PULSE_TEMPLATE)
        print(f"[pulse] created {rel(pulse, root)}")
    print(read_text(pulse).rstrip())
    return 0


def path_values(root: Path, artifact: Path) -> dict[str, str]:
    r = rel(artifact, root)
    no_ext = str(Path(r).with_suffix("")).replace("\\", "/")
    return {
        "date": today(),
        "artifact": r,
        "relative": r,
        "relative_no_ext": no_ext,
        "stem": artifact.stem,
        "name": artifact.stem,
        "audit_hash": "pending",
    }


def matching_stable_rules(cfg: dict[str, Any], artifact_rel: str) -> list[dict[str, Any]]:
    return [
        rule
        for rule in cfg.get("stable_objects", [])
        if glob_match(artifact_rel, rule.get("artifact_glob", ""))
    ]


def mirror_path(root: Path, cfg: dict[str, Any], artifact: Path, rule: dict[str, Any] | None = None) -> tuple[Path, dict[str, Any]]:
    artifact_rel = rel(artifact, root)
    if rule is None:
        matches = matching_stable_rules(cfg, artifact_rel)
        if not matches:
            raise HarnessError(
                f"no stable object rule matches {artifact_rel}; add a rule in .agentic/project.yaml "
                "or treat this as event evidence instead of a stable object"
            )
        if len(matches) > 1:
            names = ", ".join(rule.get("name", "<unnamed>") for rule in matches)
            raise HarnessError(f"ambiguous stable object rules for {artifact_rel}: {names}")
        rule = matches[0]
    values = path_values(root, artifact)
    return root / render(rule["mirror_pattern"], values), rule


def cmd_new_artifact(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    artifact = (root / args.artifact).resolve()
    if not artifact.exists():
        if args.create:
            write_text(artifact, "", force=False)
        else:
            raise SystemExit(f"artifact does not exist: {rel(artifact, root)}")

    mirror, rule = mirror_path(root, cfg, artifact)
    template = root / rule.get("template", ".agentic/templates/mirror.md")
    text = read_text(template) if template.exists() else read_text(TEMPLATES / "mirror.md")
    values = path_values(root, artifact)
    values["mirror"] = rel(mirror, root)
    created = write_text(mirror, render(text, values), force=args.force)
    print(f"[new-artifact] {'created' if created else 'exists'} {rel(mirror, root)}")
    return 0


def cmd_accept_mirror(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    artifact = (root / args.artifact).resolve()
    if not artifact.exists() or not artifact.is_file():
        raise HarnessError(f"artifact does not exist: {rel(artifact, root)}")

    mirror, _ = mirror_path(root, cfg, artifact)
    if not mirror.exists():
        raise HarnessError(f"mirror does not exist: {rel(mirror, root)}; run new-artifact first")

    text = read_text(mirror)
    updated = update_front_matter(text, {"last_audited": today(), "audit_hash": short_hash(artifact)})
    write_text(mirror, updated, force=True)
    print(f"[accept-mirror] {rel(mirror, root)} now matches {rel(artifact, root)}")
    return 0


def event_rule(cfg: dict[str, Any], name: str) -> dict[str, Any]:
    for rule in cfg.get("events", []):
        if rule.get("name") == name:
            return rule
    raise SystemExit(f"unknown event class: {name}")


def cmd_new_event(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    rule = event_rule(cfg, args.event_class)
    values = {
        "date": today(),
        "event_class": args.event_class,
        "event_id": safe_slug(args.event_id),
        "slug": safe_slug(args.slug),
        "trigger": args.trigger or "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    record_dir = root / render(rule["record_pattern"], values)
    template_dir = root / rule.get("template_dir", ".agentic/templates/event_record")
    if not template_dir.exists():
        template_dir = TEMPLATES / "event_record"
    required = rule.get("required_files", ["index.md", "input.md", "process.md", "output.md", "analysis.md", "reflux.md"])
    record_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for name in required:
        src = template_dir / name
        text = read_text(src) if src.exists() else f"# {name}\n"
        if write_text(record_dir / name, render(text, values), force=args.force):
            made.append(name)
    print(f"[new-event] {rel(record_dir, root)} ({len(made)} file(s) created)")
    return 0


@dataclass
class Issue:
    type: str
    target_artifact: str
    target_doc: str
    what: str
    resolve: str
    name: str
    severity: str = "conflict"


def front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    body = text[4:end]
    out: dict[str, Any] = {}
    current_list: str | None = None
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if line.startswith(" ") and stripped.startswith("- ") and current_list:
            out[current_list].append(parse_scalar(stripped[2:].strip()))
            continue
        current_list = None
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                out[key] = parse_scalar(value)
            else:
                out[key] = []
                current_list = key
    return out


def update_front_matter(text: str, updates: dict[str, str]) -> str:
    if not text.startswith("---\n"):
        raise HarnessError("mirror has no front matter")
    end = text.find("\n---", 4)
    if end == -1:
        raise HarnessError("front matter is not closed")

    body = text[4:end]
    rest = text[end + 4 :]
    lines = body.splitlines()
    seen: set[str] = set()
    updated_lines: list[str] = []
    for line in lines:
        if ":" in line and not line.startswith(" "):
            key = line.split(":", 1)[0].strip()
            if key in updates:
                updated_lines.append(f"{key}: {updates[key]}")
                seen.add(key)
                continue
        updated_lines.append(line)
    for key, value in updates.items():
        if key not in seen:
            updated_lines.append(f"{key}: {value}")
    return "---\n" + "\n".join(updated_lines).rstrip() + "\n---" + rest


def write_conflict(root: Path, cfg: dict[str, Any], issue: Issue) -> Path | None:
    cdir = root / cfg["conflict_dir"]
    cdir.mkdir(parents=True, exist_ok=True)
    slug = safe_slug(issue.name)
    digest = short_text_hash(f"{issue.type}|{issue.target_artifact}|{issue.target_doc}|{issue.what}")
    existing = list(cdir.glob(f"*_{slug}_{digest}.md"))
    if existing:
        return None
    path = cdir / f"{today()}_{slug}_{digest}.md"
    tmpl = root / ".agentic/templates/conflict.md"
    text = read_text(tmpl) if tmpl.exists() else read_text(TEMPLATES / "conflict.md")
    values = {
        "type": issue.type,
        "date": today(),
        "target_artifact": issue.target_artifact,
        "target_doc": issue.target_doc,
        "what": issue.what,
        "resolve": issue.resolve,
        "name": issue.name,
    }
    write_text(path, render(text, values), force=False)
    return path


def refresh_conflict_index(root: Path, cfg: dict[str, Any]) -> None:
    cdir = root / cfg["conflict_dir"]
    cdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(cdir.glob("*.md")):
        if path.name == "index.md":
            continue
        fm = front_matter(read_text(path))
        if fm.get("status", "open") == "open":
            rows.append((path, fm))

    if not rows:
        text = "# Conflict Index\n\nNo open conflicts yet.\n"
    else:
        text = "# Conflict Index\n\n| file | type | artifact | doc |\n|---|---|---|---|\n"
        for path, fm in rows:
            text += (
                f"| [{path.name}]({path.name}) | {fm.get('type', '')} | "
                f"{fm.get('target_artifact', '') or '-'} | {fm.get('target_doc', '') or '-'} |\n"
            )
    write_text(cdir / "index.md", text, force=True)


def audit_stable(root: Path, cfg: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    artifact_rels: set[str] = set()

    for rule in cfg.get("stable_objects", []):
        for artifact in sorted(root.glob(rule.get("artifact_glob", ""))):
            if not artifact.is_file():
                continue
            artifact_rel = rel(artifact, root)
            artifact_rels.add(artifact_rel)

    for artifact_rel in sorted(artifact_rels):
        artifact = root / artifact_rel
        matches = matching_stable_rules(cfg, artifact_rel)
        if not matches:
            issues.append(Issue("unconfigured-artifact", artifact_rel, "", f"{artifact_rel} matched no stable rule during audit.", "Fix .agentic/project.yaml.", f"{artifact.stem}_unconfigured"))
            continue
        if len(matches) > 1:
            names = ", ".join(rule.get("name", "<unnamed>") for rule in matches)
            issues.append(Issue("ambiguous-rule", artifact_rel, "", f"{artifact_rel} matches multiple stable rules: {names}.", "Make stable object globs non-overlapping.", f"{artifact.stem}_ambiguous_rule"))
            continue

        mirror, _ = mirror_path(root, cfg, artifact, matches[0])
        mirror_rel = rel(mirror, root)
        if not mirror.exists():
            issues.append(Issue("uncovered-artifact", artifact_rel, mirror_rel, f"{artifact_rel} has no mirror doc.", "Run new-artifact or mark it exempt.", f"{artifact.stem}_uncovered"))
            continue
        text = read_text(mirror)
        fm = front_matter(text)
        if not fm:
            issues.append(Issue("no-front-matter", artifact_rel, mirror_rel, f"{mirror_rel} has no front matter.", "Add mirror front matter.", f"{mirror.stem}_no_front_matter"))
            continue
        recorded = str(fm.get("audit_hash", "")).strip()
        current = short_hash(artifact)
        if not recorded:
            issues.append(Issue("no-audit-hash", artifact_rel, mirror_rel, f"{mirror_rel} has no audit_hash.", "Review mirror, then run accept-mirror.", f"{mirror.stem}_no_hash"))
        elif recorded == "pending":
            issues.append(Issue("pending-mirror-review", artifact_rel, mirror_rel, f"{mirror_rel} has not been accepted against the artifact yet.", "Review mirror, then run accept-mirror.", f"{mirror.stem}_pending_review", severity="pending"))
        elif recorded != current:
            issues.append(Issue("artifact-vs-doc", artifact_rel, mirror_rel, f"{artifact_rel} hash changed: {recorded} -> {current}.", "Review artifact; update mirror or run accept-mirror after review.", f"{mirror.stem}_drift"))

    mirror_root = root / cfg["semantic_root"] / "field" / "mirrors"
    if mirror_root.exists():
        for mirror in sorted(mirror_root.rglob("*.md")):
            text = read_text(mirror)
            fm = front_matter(text)
            covers_value = fm.get("covers", [])
            covers = covers_value if isinstance(covers_value, list) else [str(covers_value)]
            for covered in [c.strip() for c in covers if c.strip()]:
                if covered and not (root / covered).exists():
                    issues.append(Issue("orphan-doc", covered, rel(mirror, root), f"{rel(mirror, root)} covers missing artifact {covered}.", "Restore artifact or move doc to removed/archive.", f"{mirror.stem}_orphan"))
    return issues


def record_pattern_regex(pattern: str) -> re.Pattern[str]:
    token = r"[A-Za-z0-9_\-\u4e00-\u9fff]+"
    out = []
    i = 0
    while i < len(pattern):
        if pattern[i] == "{":
            j = pattern.find("}", i + 1)
            if j == -1:
                raise HarnessError(f"unclosed placeholder in record_pattern: {pattern}")
            name = pattern[i + 1 : j]
            out.append(r"\d{4}-\d{2}-\d{2}" if name == "date" else token)
            i = j + 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def audit_events(root: Path, cfg: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    for rule in cfg.get("events", []):
        # Use the static prefix before placeholders to find record folders.
        prefix = rule.get("record_pattern", "").split("{", 1)[0].rstrip("/")
        base = root / prefix
        if not base.exists():
            continue
        pattern = record_pattern_regex(rule.get("record_pattern", ""))
        required = rule.get("required_files", [])
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            folder_rel = rel(folder, root)
            if not pattern.match(folder_rel):
                issues.append(Issue("record-name-out-of-schema", "", folder_rel, f"{folder_rel} does not match record_pattern.", "Rename the folder or adjust .agentic/project.yaml.", f"{folder.name}_bad_record_name"))
                continue
            missing = [name for name in required if not (folder / name).exists()]
            if missing:
                issues.append(Issue("incomplete-record", "", folder_rel, f"{folder_rel} is missing: {', '.join(missing)}.", "Create missing record files from template.", f"{folder.name}_incomplete"))
            reflux = folder / "reflux.md"
            if reflux.exists():
                verdict = str(front_matter(read_text(reflux)).get("verdict", "")).strip()
                if verdict == "pending":
                    issues.append(Issue("pending-reflux", "", rel(reflux, root), f"{rel(reflux, root)} is still pending.", "Accept/reject/supersede after human/agent interpretation.", f"{folder.name}_pending_reflux", severity="pending"))
    return issues


def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    issues = audit_stable(root, cfg) + audit_events(root, cfg)
    if not issues:
        print("[audit] clean")
        refresh_conflict_index(root, cfg)
        return 0
    conflicts = [issue for issue in issues if issue.severity == "conflict"]
    pending = [issue for issue in issues if issue.severity != "conflict"]
    print(f"[audit] {len(conflicts)} conflict(s), {len(pending)} pending item(s)")
    for issue in issues:
        label = issue.type if issue.severity == "conflict" else f"{issue.type}:pending"
        print(f"  [{label}] {issue.target_artifact or '-'} :: {issue.target_doc or '-'}")
    if conflicts and not args.no_conflicts:
        written = 0
        for issue in conflicts:
            if write_conflict(root, cfg, issue):
                written += 1
        refresh_conflict_index(root, cfg)
        print(f"[audit] wrote {written} conflict file(s)")
    else:
        refresh_conflict_index(root, cfg)
    return 1 if conflicts else 0


def cmd_reflux_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    base = root / cfg["semantic_root"] / "records"
    pending = []
    if base.exists():
        for path in base.rglob("reflux.md"):
            verdict = str(front_matter(read_text(path)).get("verdict", "")).strip()
            if verdict == "pending":
                pending.append(path)
    if not pending:
        print("[reflux-check] clean")
        return 0
    print(f"[reflux-check] {len(pending)} pending reflux file(s):")
    for path in pending:
        print(f"  {rel(path, root)}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agentic structural harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("init")
    q.add_argument("--root", default=".")
    q.add_argument("--force", action="store_true")
    q.set_defaults(func=cmd_init)

    q = sub.add_parser("pulse")
    q.add_argument("--root", default=".")
    q.set_defaults(func=cmd_pulse)

    q = sub.add_parser("new-artifact")
    q.add_argument("artifact")
    q.add_argument("--root", default=".")
    q.add_argument("--create", action="store_true")
    q.add_argument("--force", action="store_true")
    q.set_defaults(func=cmd_new_artifact)

    q = sub.add_parser("accept-mirror")
    q.add_argument("artifact")
    q.add_argument("--root", default=".")
    q.set_defaults(func=cmd_accept_mirror)

    q = sub.add_parser("new-event")
    q.add_argument("event_class")
    q.add_argument("--id", dest="event_id", required=True)
    q.add_argument("--slug", required=True)
    q.add_argument("--trigger", default="")
    q.add_argument("--root", default=".")
    q.add_argument("--force", action="store_true")
    q.set_defaults(func=cmd_new_event)

    q = sub.add_parser("audit")
    q.add_argument("--root", default=".")
    q.add_argument("--no-conflicts", action="store_true")
    q.set_defaults(func=cmd_audit)

    q = sub.add_parser("reflux-check")
    q.add_argument("--root", default=".")
    q.set_defaults(func=cmd_reflux_check)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
