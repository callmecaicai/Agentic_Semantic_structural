#!/usr/bin/env python3
"""Lightweight agentic structural harness. No external dependencies."""

from __future__ import annotations

import argparse
import fnmatch
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
TODAY = date.today().isoformat()


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
    return hashlib.sha1(path.read_bytes()).hexdigest()[:7]


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


def load_yaml_subset(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    current_list: list[dict[str, Any]] | None = None
    current_item: dict[str, Any] | None = None
    current_sublist: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
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
                out[key.strip()] = value.strip()
            continue

        if indent == 2 and stripped.startswith("- ") and current_list is not None:
            current_item = {}
            current_list.append(current_item)
            current_sublist = None
            rest = stripped[2:].strip()
            if rest and ":" in rest:
                key, value = rest.split(":", 1)
                current_item[key.strip()] = value.strip()
            continue

        if indent == 4 and current_item is not None:
            if stripped.endswith(":"):
                key = stripped[:-1].strip()
                current_item[key] = []
                current_sublist = key
            elif ":" in stripped:
                key, value = stripped.split(":", 1)
                current_item[key.strip()] = value.strip()
                current_sublist = None
            continue

        if indent == 6 and stripped.startswith("- ") and current_item is not None and current_sublist:
            current_item[current_sublist].append(stripped[2:].strip())

    return out


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
        "date": TODAY,
        "artifact": r,
        "relative": r,
        "relative_no_ext": no_ext,
        "stem": artifact.stem,
        "name": artifact.stem,
        "audit_hash": short_hash(artifact) if artifact.exists() and artifact.is_file() else "",
    }


def find_stable_rule(cfg: dict[str, Any], artifact_rel: str) -> dict[str, Any] | None:
    for rule in cfg.get("stable_objects", []):
        pat = rule.get("artifact_glob", "")
        if fnmatch.fnmatch(artifact_rel, pat):
            return rule
    return None


def mirror_path(root: Path, cfg: dict[str, Any], artifact: Path) -> tuple[Path, dict[str, Any]]:
    artifact_rel = rel(artifact, root)
    rule = find_stable_rule(cfg, artifact_rel)
    if rule is None:
        no_ext = str(Path(artifact_rel).with_suffix("")).replace("\\", "/")
        rule = {
            "name": "default",
            "mirror_pattern": f"{cfg['semantic_root']}/field/mirrors/{no_ext}.md",
            "template": ".agentic/templates/mirror.md",
        }
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
        "date": TODAY,
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
            out[current_list].append(stripped[2:].strip())
            continue
        current_list = None
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                out[key] = value
            else:
                out[key] = []
                current_list = key
    return out


def write_conflict(root: Path, cfg: dict[str, Any], issue: Issue) -> Path | None:
    cdir = root / cfg["conflict_dir"]
    cdir.mkdir(parents=True, exist_ok=True)
    path = cdir / f"{TODAY}_{safe_slug(issue.name)}.md"
    if path.exists():
        return None
    tmpl = root / ".agentic/templates/conflict.md"
    text = read_text(tmpl) if tmpl.exists() else read_text(TEMPLATES / "conflict.md")
    values = {
        "type": issue.type,
        "date": TODAY,
        "target_artifact": issue.target_artifact,
        "target_doc": issue.target_doc,
        "what": issue.what,
        "resolve": issue.resolve,
        "name": issue.name,
    }
    write_text(path, render(text, values), force=False)
    return path


def audit_stable(root: Path, cfg: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    artifacts_seen: set[str] = set()

    for rule in cfg.get("stable_objects", []):
        for artifact in sorted(root.glob(rule.get("artifact_glob", ""))):
            if not artifact.is_file():
                continue
            artifact_rel = rel(artifact, root)
            artifacts_seen.add(artifact_rel)
            mirror, _ = mirror_path(root, cfg, artifact)
            mirror_rel = rel(mirror, root)
            if not mirror.exists():
                issues.append(Issue("uncovered-artifact", artifact_rel, mirror_rel, f"{artifact_rel} has no mirror doc.", "Run new-artifact or mark it exempt.", f"{artifact.stem}_uncovered"))
                continue
            text = read_text(mirror)
            fm = front_matter(text)
            if not fm:
                issues.append(Issue("no-front-matter", artifact_rel, mirror_rel, f"{mirror_rel} has no front matter.", "Add mirror front matter.", f"{mirror.stem}_no_front_matter"))
                continue
            recorded = fm.get("audit_hash", "").strip()
            current = short_hash(artifact)
            if not recorded:
                issues.append(Issue("no-audit-hash", artifact_rel, mirror_rel, f"{mirror_rel} has no audit_hash.", "Initialize audit_hash after reviewing doc.", f"{mirror.stem}_no_hash"))
            elif recorded != current:
                issues.append(Issue("artifact-vs-doc", artifact_rel, mirror_rel, f"{artifact_rel} hash changed: {recorded} -> {current}.", "Review artifact; update mirror or hash.", f"{mirror.stem}_drift"))

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


def audit_events(root: Path, cfg: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    for rule in cfg.get("events", []):
        # Use the static prefix before placeholders to find record folders.
        prefix = rule.get("record_pattern", "").split("{", 1)[0].rstrip("/")
        base = root / prefix
        if not base.exists():
            continue
        required = rule.get("required_files", [])
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            missing = [name for name in required if not (folder / name).exists()]
            if missing:
                issues.append(Issue("incomplete-record", "", rel(folder, root), f"{rel(folder, root)} is missing: {', '.join(missing)}.", "Create missing record files from template.", f"{folder.name}_incomplete"))
            reflux = folder / "reflux.md"
            if reflux.exists() and "verdict: pending" in read_text(reflux):
                issues.append(Issue("evidence-not-refluxed", "", rel(reflux, root), f"{rel(reflux, root)} is still pending.", "Accept/reject/supersede evidence or create conflict.", f"{folder.name}_pending_reflux"))
    return issues


def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    issues = audit_stable(root, cfg) + audit_events(root, cfg)
    if not issues:
        print("[audit] clean")
        return 0
    print(f"[audit] {len(issues)} issue(s)")
    for issue in issues:
        print(f"  [{issue.type}] {issue.target_artifact or '-'} :: {issue.target_doc or '-'}")
    if not args.no_conflicts:
        written = 0
        for issue in issues:
            if write_conflict(root, cfg, issue):
                written += 1
        print(f"[audit] wrote {written} conflict file(s)")
    return 1


def cmd_reflux_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cfg = config(root)
    base = root / cfg["semantic_root"] / "records"
    pending = []
    if base.exists():
        for path in base.rglob("reflux.md"):
            if "verdict: pending" in read_text(path):
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
