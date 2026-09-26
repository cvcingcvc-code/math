#!/usr/bin/env python3
"""Small, file-backed coordinator for the competition's Codex windows.

The project state is human-readable Markdown with a JSON block.  Updates use a
short exclusive lock and an atomic replace so two Codex processes cannot
silently overwrite one another.  The script deliberately has no server,
database, dependency, or background process.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


# Project-relative default: resolves to the repo root (this file lives in scripts/).
# Override per-invocation with `--root <path>` if running against another checkout.
DEFAULT_ROOT = Path(__file__).resolve().parents[1]
STATE_RELATIVE = Path("handoff") / "MULTIPROCESS_STATE.md"
JSON_START = "<!-- MULTIPROCESS_STATE_JSON_START -->"
JSON_END = "<!-- MULTIPROCESS_STATE_JSON_END -->"
LOCK_STALE_SECONDS = 120

WINDOW_STATUSES = {
    "REGISTERED",
    "RUNNING",
    "WAITING",
    "BLOCKED",
    "HANDOFF_READY",
    "HANDOFF_COMPLETE",
    "FROZEN",
    "CLOSED",
}
MODES = {"READONLY", "WRITE", "MAIN_RESEARCH"}
TERMINAL_WORKSTREAM_STATUSES = {"FROZEN", "HANDOFF_COMPLETE", "DONE"}

WORKSTREAMS = [
    "MAIN_RESEARCH",
    "BASELINE",
    "ML_CHALLENGER",
    "ALTERNATIVE_FORMULATIONS",
    "EXTERNAL_TRANSFER",
    "AUDIT",
    "LITERATURE",
    "FIGURES",
    "DEMO_UI",
    "PAPER",
    "PPT",
    "MODEL_PRESENTATION",
    "HUMAN_GATE",
    "FORMAL_VALIDATION",
    "SUBMISSION",
]

DEFAULT_SCOPES = {
    "MAIN_RESEARCH": "CORE_MODEL",
    "BASELINE": "CORE_MODEL",
    "ML_CHALLENGER": "CORE_MODEL",
    "ALTERNATIVE_FORMULATIONS": "CORE_MODEL",
    "EXTERNAL_TRANSFER": "CORE_MODEL",
    "PAPER": "PAPER",
    "DEMO_UI": "DEMO_UI",
    "HUMAN_GATE": "HUMAN_LABELS",
    "FORMAL_VALIDATION": "FORMAL_GATE",
    "FIGURES": "FIGURES_FINAL",
    "PPT": "PPT_FINAL",
    "MODEL_PRESENTATION": "PPT_FINAL",
    "SUBMISSION": "SUBMISSION_FILES",
}


class ManagerError(RuntimeError):
    """An expected user-facing coordination error."""


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def clean(value: Optional[str]) -> str:
    return (value or "").strip()


def slug(value: str) -> str:
    return re.sub(r"[^A-Z0-9_]+", "_", value.upper()).strip("_")


def git_value(root: Path, args: List[str], fallback: str = "UNKNOWN") -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return result.stdout.strip() or fallback
    except (OSError, subprocess.CalledProcessError):
        return fallback


def ensure_project_identity(root: Path) -> None:
    root = root.resolve()
    if not root.is_dir():
        raise ManagerError(f"PROJECT_NOT_FOUND\n{root}")
    agents = root / "AGENTS.md"
    if not agents.is_file():
        raise ManagerError(
            "PROJECT_IDENTITY_UNCONFIRMED\n"
            f"Expected AGENTS.md at {agents}"
        )
    text = agents.read_text(encoding="utf-8", errors="replace")
    markers = ("数学建模", "2026-09-25\\yu", "新时代教育中 AI 增量价值评价")
    if not any(marker in text for marker in markers):
        raise ManagerError(
            "PROJECT_IDENTITY_UNCONFIRMED\n"
            "AGENTS.md does not identify the competition project"
        )


def default_workstreams() -> Dict[str, Dict[str, Any]]:
    return {
        role: {
            "status": "NOT_STARTED",
            "owner": None,
            "task": "",
            "mode": None,
            "write_scope": None,
            "priority": "P2",
            "dependency": None,
            "evidence": "",
            "risk": "",
        }
        for role in WORKSTREAMS
    }


def empty_state(root: Path) -> Dict[str, Any]:
    return {
        "PROJECT": str(root.resolve()),
        "STATUS": "UNINITIALIZED",
        "LAST_UPDATED": now_iso(),
        "MAIN_WINDOW": None,
        "CURRENT_PHASE": "UNKNOWN",
        "FORMAL_GATE_STATUS": "UNKNOWN",
        "HUMAN_GATE_STATUS": "UNKNOWN",
        "ACTIVE_WINDOWS": [],
        "COMPLETED_WORKSTREAMS": [],
        "FROZEN_WORKSTREAMS": [],
        "WRITE_LOCKS": {},
        "READONLY_TASKS": [],
        "PENDING_HANDOFFS": [],
        "KNOWN_RISKS": [],
        "NEXT_ALLOWED_TASKS": [],
        "WORKSTREAMS": default_workstreams(),
        "WINDOW_HISTORY": [],
    }


def state_path(root: Path, explicit: Optional[str]) -> Path:
    return Path(explicit).expanduser().resolve() if explicit else (root / STATE_RELATIVE).resolve()


def read_state(path: Path, root: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ManagerError(
            "STATE_NOT_FOUND\n"
            f"Expected {path}\n"
            "Run `python scripts/project_manager.py init` after confirming project identity."
        )
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        re.escape(JSON_START) + r"\s*\n(.*?)\n\s*" + re.escape(JSON_END),
        raw,
        flags=re.DOTALL,
    )
    if not match:
        raise ManagerError(f"STATE_FORMAT_ERROR\nNo JSON state block found in {path}")
    try:
        state = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ManagerError(f"STATE_FORMAT_ERROR\n{exc}") from exc
    if not isinstance(state, dict):
        raise ManagerError("STATE_FORMAT_ERROR\nTop-level state must be an object")
    state.setdefault("WORKSTREAMS", {})
    state.setdefault("ACTIVE_WINDOWS", [])
    state.setdefault("WINDOW_HISTORY", [])
    state.setdefault("WRITE_LOCKS", {})
    return state


def state_json(state: Dict[str, Any]) -> str:
    return json.dumps(state, ensure_ascii=False, indent=2, sort_keys=False)


def render_state(state: Dict[str, Any]) -> str:
    workstreams = state.get("WORKSTREAMS", {})
    active = state.get("ACTIVE_WINDOWS", [])
    locks = state.get("WRITE_LOCKS", {})
    lines = [
        "# MULTIPROCESS STATE",
        "",
        "> Single Source of Truth for Codex windows working on the competition project.",
        "> Read this file after the canonical handoff files. Edit it through `scripts/project_manager.py` when possible.",
        "",
        f"- PROJECT: `{state.get('PROJECT', '')}`",
        f"- STATUS: `{state.get('STATUS', '')}`",
        f"- LAST_UPDATED: `{state.get('LAST_UPDATED', '')}`",
        f"- MAIN_WINDOW: `{state.get('MAIN_WINDOW') or 'NONE'}`",
        f"- CURRENT_PHASE: `{state.get('CURRENT_PHASE', '')}`",
        f"- FORMAL_GATE_STATUS: `{state.get('FORMAL_GATE_STATUS', '')}`",
        f"- HUMAN_GATE_STATUS: `{state.get('HUMAN_GATE_STATUS', '')}`",
        "",
        "## WORKSTREAMS",
        "",
        "| Workstream | Status | Owner | Task | Evidence / boundary |",
        "|---|---|---|---|---|",
    ]
    for role in WORKSTREAMS:
        item = workstreams.get(role, {})
        evidence = str(item.get("evidence", "")).replace("|", "\\|").replace("\n", " ")
        task = str(item.get("task", "")).replace("|", "\\|").replace("\n", " ")
        owner = item.get("owner") or "-"
        lines.append(f"| {role} | {item.get('status', 'NOT_STARTED')} | {owner} | {task} | {evidence} |")
    lines += [
        "",
        "## ACTIVE_WINDOWS",
        "",
        "| Window | Role | Mode | Status | Scope | Task | Last update |",
        "|---|---|---|---|---|---|---|",
    ]
    if active:
        for item in active:
            task = str(item.get("task", "")).replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| {item.get('window_id')} | {item.get('role')} | {item.get('mode')} | "
                f"{item.get('status')} | {item.get('write_scope') or '-'} | {task} | {item.get('last_update', '')} |"
            )
    else:
        lines.append("| NONE | - | - | - | - | No registered windows | - |")
    lines += ["", "## WRITE_LOCKS", "", "| Scope | Owner |", "|---|---|"]
    if locks:
        for scope, owner in locks.items():
            lines.append(f"| {scope} | {owner} |")
    else:
        lines.append("| NONE | FREE |")
    lines += ["", "## READONLY_TASKS", ""]
    readonly = state.get("READONLY_TASKS", [])
    if readonly:
        lines.extend(f"- {item}" for item in readonly)
    else:
        lines.append("- Red-team audit, literature review, claim checks, figure planning, failure-case checks, reproducibility checks, and file-consistency checks may run in separate output paths.")
    lines += ["", "## PENDING_HANDOFFS", ""]
    pending = state.get("PENDING_HANDOFFS", [])
    lines.extend(f"- {item}" for item in pending) if pending else lines.append("- None")
    lines += ["", "## KNOWN_RISKS", ""]
    risks = state.get("KNOWN_RISKS", [])
    lines.extend(f"- {item}" for item in risks) if risks else lines.append("- None recorded")
    lines += ["", "## NEXT_ALLOWED_TASKS", ""]
    next_tasks = state.get("NEXT_ALLOWED_TASKS", [])
    lines.extend(f"- {item}" for item in next_tasks) if next_tasks else lines.append("- None recorded")
    lines += [
        "",
        "## MACHINE_STATE",
        "",
        JSON_START,
        state_json(state),
        JSON_END,
        "",
    ]
    return "\n".join(lines)


class StateLock:
    def __init__(self, lock_path: Path, timeout: float = 15.0) -> None:
        self.lock_path = lock_path
        self.timeout = timeout
        self.fd: Optional[int] = None

    def __enter__(self) -> "StateLock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self.fd = os.open(
                    str(self.lock_path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
                os.write(self.fd, f"pid={os.getpid()}\ncreated={now_iso()}\n".encode("utf-8"))
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.lock_path.stat().st_mtime
                    if age > LOCK_STALE_SECONDS:
                        self.lock_path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise ManagerError(
                        "STATE_LOCK_BUSY\n"
                        f"Another process is updating {self.lock_path.parent / STATE_RELATIVE.name}. "
                        "Wait briefly and retry."
                    )
                time.sleep(0.1)

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass


def write_state(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["LAST_UPDATED"] = now_iso()
    content = render_state(state)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        tmp.write_text(content, encoding="utf-8", newline="\n")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def load_for_mutation(path: Path, root: Path) -> Dict[str, Any]:
    return read_state(path, root)


def find_window(state: Dict[str, Any], window_id: str) -> Dict[str, Any]:
    for item in state.get("ACTIVE_WINDOWS", []):
        if item.get("window_id") == window_id:
            return item
    raise ManagerError(f"WINDOW_NOT_FOUND\n{window_id}")


def active_owner(state: Dict[str, Any], scope: str) -> Optional[Dict[str, Any]]:
    owner_id = state.get("WRITE_LOCKS", {}).get(scope)
    if not owner_id:
        return None
    for item in state.get("ACTIVE_WINDOWS", []):
        if item.get("window_id") == owner_id:
            return item
    return {"window_id": owner_id, "role": "UNKNOWN", "task": "stale lock record"}


def next_window_id(state: Dict[str, Any]) -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    used = {item.get("window_id") for item in state.get("ACTIVE_WINDOWS", [])}
    used.update(item.get("window_id") for item in state.get("WINDOW_HISTORY", []))
    base = f"WINDOW_{stamp}"
    candidate = base
    suffix = 1
    while candidate in used:
        suffix += 1
        candidate = f"{base}_{suffix:02d}"
    return candidate


def registration_conflict(state: Dict[str, Any], role: str, mode: str, scope: Optional[str], reopen: bool) -> None:
    work = state.get("WORKSTREAMS", {}).get(role, {})
    status = str(work.get("status", "NOT_STARTED")).upper()
    if status in TERMINAL_WORKSTREAM_STATUSES and mode != "READONLY" and not reopen and role != "MAIN_RESEARCH":
        raise ManagerError(
            "DUPLICATE_OR_FROZEN\n"
            f"{role} is currently {status}.\n"
            "Read the existing handoff before creating work.\n"
            "Only MAIN_RESEARCH may authorize an explicit supplement with --reopen."
        )
    if reopen and role != "MAIN_RESEARCH":
        raise ManagerError("REOPEN_NOT_ALLOWED\nOnly MAIN_RESEARCH may create a new evidence supplement.")
    if mode in {"WRITE", "MAIN_RESEARCH"} and scope:
        owner = active_owner(state, scope)
        if owner:
            raise ManagerError(
                "CONFLICT\n\n"
                f"{scope} is currently owned by {owner.get('window_id')} ({owner.get('role')}).\n\n"
                "Allowed actions:\n"
                "- READONLY audit\n"
                "- choose another workstream\n"
                "- wait for lock release"
            )
    if mode == "MAIN_RESEARCH" and state.get("MAIN_WINDOW"):
        owner_id = state.get("MAIN_WINDOW")
        if any(item.get("window_id") == owner_id for item in state.get("ACTIVE_WINDOWS", [])):
            raise ManagerError(
                "CONFLICT\n\n"
                f"MAIN_RESEARCH is currently owned by {owner_id}.\n"
                "Only one MAIN_RESEARCH window may be active."
            )


def cmd_identify(root: Path) -> int:
    try:
        ensure_project_identity(root)
    except ManagerError as exc:
        print(str(exc))
        return 2
    fixed_files = [
        root / "AGENTS.md",
        root / "README.md",
        root / "handoff" / "PROJECT_STATE.md",
        root / "handoff" / "PROJECT_NOW.md",
    ]
    keywords = [
        "MAIN_RESEARCH",
        "CONVERGENCE",
        "Evidence Reliability",
        "Raw Signal",
        "Adjusted Evaluation",
        "Human Gate",
        "Formal Gate",
        "数学建模",
    ]
    haystack = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in fixed_files
        if path.is_file()
    )
    hits = [keyword for keyword in keywords if keyword.lower() in haystack.lower()]
    print("PROJECT_MATCH")
    print(f"ROOT {root.resolve()}")
    print(f"KEYWORD_HITS {len(hits)}/{len(keywords)}")
    print("RECURSIVE_SCAN false")
    return 0


def cmd_init(root: Path, path: Path, force: bool) -> int:
    ensure_project_identity(root)
    if path.exists() and not force:
        print(f"STATE_EXISTS\n{path}")
        return 0
    with StateLock(path.with_suffix(path.suffix + ".lock")):
        state = empty_state(root)
        write_state(path, state)
    print(f"STATE_INITIALIZED\n{path}")
    return 0


def cmd_status(root: Path, path: Path, as_json: bool) -> int:
    ensure_project_identity(root)
    state = read_state(path, root)
    if as_json:
        print(state_json(state))
        return 0
    print(f"PROJECT {state.get('PROJECT', root)}")
    print(f"STATUS {state.get('STATUS', 'UNKNOWN')}")
    print(f"PHASE {state.get('CURRENT_PHASE', 'UNKNOWN')}")
    print(f"MAIN_WINDOW {state.get('MAIN_WINDOW') or 'FREE'}")
    print(f"HUMAN_GATE {state.get('HUMAN_GATE_STATUS', 'UNKNOWN')}")
    print(f"FORMAL_GATE {state.get('FORMAL_GATE_STATUS', 'UNKNOWN')}")
    print("\nWORKSTREAMS")
    for role in WORKSTREAMS:
        item = state.get("WORKSTREAMS", {}).get(role, {})
        print(f"{role:<24} {item.get('status', 'NOT_STARTED')}")
    print("\nWRITE LOCKS")
    scopes = sorted(set(DEFAULT_SCOPES.values()) | set(state.get("WRITE_LOCKS", {}).keys()))
    for scope in scopes:
        print(f"{scope:<20} {state.get('WRITE_LOCKS', {}).get(scope, 'FREE')}")
    print("\nACTIVE WINDOWS")
    active = state.get("ACTIVE_WINDOWS", [])
    if not active:
        print("NONE")
    else:
        for item in active:
            print(
                f"{item.get('window_id')}  {item.get('role')}  {item.get('mode')}  "
                f"{item.get('status')}  scope={item.get('write_scope') or '-'}"
            )
    return 0


def cmd_register(root: Path, path: Path, args: argparse.Namespace) -> int:
    ensure_project_identity(root)
    role = clean(args.role).upper()
    mode = clean(args.mode).upper()
    if role not in WORKSTREAMS:
        raise ManagerError(f"UNKNOWN_ROLE\n{role}\nAllowed: {', '.join(WORKSTREAMS)}")
    if mode not in MODES:
        raise ManagerError(f"UNKNOWN_MODE\n{mode}\nAllowed: {', '.join(sorted(MODES))}")
    if mode == "MAIN_RESEARCH" and role != "MAIN_RESEARCH":
        raise ManagerError("MODE_ROLE_MISMATCH\nMAIN_RESEARCH mode requires role MAIN_RESEARCH")
    if role == "HUMAN_GATE" and mode == "WRITE":
        raise ManagerError(
            "BLOCKED\nHUMAN_GATE write access is reserved for the human owner; do not fill or alter R1/R2."
        )
    if role == "FORMAL_VALIDATION" and mode == "WRITE":
        raise ManagerError(
            "BLOCKED\nFORMAL_VALIDATION is fail-closed until the real Human Gate passes."
        )
    if mode == "READONLY" and args.write_scope:
        raise ManagerError("INVALID_SCOPE\nREADONLY windows do not acquire a write scope")
    scope = None
    if mode in {"WRITE", "MAIN_RESEARCH"}:
        scope = clean(args.write_scope).upper() or DEFAULT_SCOPES.get(role)
        if not scope:
            raise ManagerError(
                "WRITE_SCOPE_REQUIRED\n"
                f"Role {role} has no default scope; use --write-scope with an independent output area."
            )
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,63}", scope):
            raise ManagerError("INVALID_SCOPE\nUse uppercase letters, digits, and underscores (2–64 chars).")
    with StateLock(path.with_suffix(path.suffix + ".lock")):
        state = load_for_mutation(path, root)
        registration_conflict(state, role, mode, scope, bool(args.reopen))
        window_id = clean(args.window_id).upper() or next_window_id(state)
        if any(item.get("window_id") == window_id for item in state.get("ACTIVE_WINDOWS", [])):
            raise ManagerError(f"WINDOW_EXISTS\n{window_id}")
        task = clean(args.task) or "Unspecified task; read handoff and define a bounded task before editing."
        handoff_path = clean(args.handoff_path)
        if not handoff_path:
            handoff_path = str(Path("handoff") / "multiprocess" / f"{window_id}.md")
        item = {
            "window_id": window_id,
            "role": role,
            "task": task,
            "mode": mode,
            "status": "REGISTERED",
            "write_scope": scope,
            "started_at": now_iso(),
            "last_update": now_iso(),
            "handoff_path": handoff_path,
            "pid": os.getpid(),
            "cwd": str(Path.cwd()),
            "workstream_status_before": state.get("WORKSTREAMS", {}).get(role, {}).get("status", "NOT_STARTED"),
        }
        state.setdefault("ACTIVE_WINDOWS", []).append(item)
        if scope:
            state.setdefault("WRITE_LOCKS", {})[scope] = window_id
        if role == "MAIN_RESEARCH":
            state["MAIN_WINDOW"] = window_id
        # A read-only audit must not turn an already FROZEN/HANDOFF_COMPLETE
        # workstream back into RUNNING.  The active-window row is sufficient
        # to show that the audit is in progress.
        if mode != "READONLY":
            work = state.setdefault("WORKSTREAMS", {}).setdefault(role, {})
            work.update({"status": "RUNNING", "owner": window_id, "task": task, "mode": mode, "write_scope": scope})
        write_state(path, state)
    print(f"REGISTERED\nWINDOW_ID {window_id}\nROLE {role}\nMODE {mode}\nSCOPE {scope or 'READONLY'}")
    return 0


def cmd_update(root: Path, path: Path, args: argparse.Namespace) -> int:
    ensure_project_identity(root)
    status = clean(args.status).upper()
    if status not in WINDOW_STATUSES:
        raise ManagerError(f"UNKNOWN_STATUS\n{status}\nAllowed: {', '.join(sorted(WINDOW_STATUSES))}")
    with StateLock(path.with_suffix(path.suffix + ".lock")):
        state = load_for_mutation(path, root)
        item = find_window(state, args.window_id)
        item["status"] = status
        item["last_update"] = now_iso()
        if args.task:
            item["task"] = clean(args.task)
        if status == "HANDOFF_READY":
            handoffs = state.setdefault("PENDING_HANDOFFS", [])
            marker = f"{item.get('window_id')}: {item.get('handoff_path')}"
            if marker not in handoffs:
                handoffs.append(marker)
        write_state(path, state)
    print(f"UPDATED\n{args.window_id} {status}")
    return 0


def split_files(value: str) -> List[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def cmd_handoff(root: Path, path: Path, args: argparse.Namespace) -> int:
    ensure_project_identity(root)
    final_status = "FROZEN" if args.freeze else "HANDOFF_COMPLETE"
    with StateLock(path.with_suffix(path.suffix + ".lock")):
        state = load_for_mutation(path, root)
        item = find_window(state, args.window_id)
        handoff_rel = clean(args.handoff_path) or item.get("handoff_path") or str(
            Path("handoff") / "multiprocess" / f"{args.window_id}.md"
        )
        handoff_path = (root / handoff_rel).resolve() if not Path(handoff_rel).is_absolute() else Path(handoff_rel)
        handoff_path.parent.mkdir(parents=True, exist_ok=True)
        if handoff_path.exists() and not args.force:
            raise ManagerError(f"HANDOFF_EXISTS\n{handoff_path}\nUse --force only to replace the same window's handoff.")
        body = [
            f"# WINDOW HANDOFF — {item.get('window_id')}",
            "",
            f"WINDOW: {item.get('window_id')}",
            f"ROLE: {item.get('role')}",
            f"TASK: {item.get('task')}",
            f"STATUS: {final_status}",
            "",
            f"FILES_CREATED: {args.files_created or 'None'}",
            f"FILES_MODIFIED: {args.files_modified or 'None'}",
            "",
            f"RESULTS: {args.results or 'Not supplied'}",
            f"CAN_MAIN_RESEARCH_USE: {args.can_main_research_use or 'NO'}",
            f"CLAIM_BOUNDARY: {args.claim_boundary or 'Use only evidence recorded in the handoff and canonical files.'}",
            f"KNOWN_PROBLEMS: {args.known_problems or 'None recorded'}",
            f"NEXT_ACTION: {args.next_action or 'Read the canonical handoff before another task.'}",
            f"WRITE_LOCK_RELEASED: YES",
            f"COMPLETED_AT: {now_iso()}",
            "",
        ]
        handoff_path.write_text("\n".join(body), encoding="utf-8", newline="\n")
        active = state.get("ACTIVE_WINDOWS", [])
        state["ACTIVE_WINDOWS"] = [entry for entry in active if entry.get("window_id") != args.window_id]
        scope = item.get("write_scope")
        if scope and state.get("WRITE_LOCKS", {}).get(scope) == args.window_id:
            state["WRITE_LOCKS"].pop(scope, None)
        if state.get("MAIN_WINDOW") == args.window_id:
            state["MAIN_WINDOW"] = None
        state.setdefault("PENDING_HANDOFFS", [])[:] = [
            marker for marker in state.get("PENDING_HANDOFFS", []) if not marker.startswith(f"{args.window_id}:")
        ]
        item = dict(item)
        item.update({"status": final_status, "last_update": now_iso(), "handoff_path": str(handoff_path)})
        state.setdefault("WINDOW_HISTORY", []).append(item)
        role = item.get("role")
        if item.get("mode") != "READONLY":
            work = state.setdefault("WORKSTREAMS", {}).setdefault(role, {})
            work.update({"status": final_status, "owner": None, "mode": item.get("mode"), "write_scope": None})
        write_state(path, state)
    print(f"HANDOFF_COMPLETE\nWINDOW_ID {args.window_id}\nSTATUS {final_status}\nHANDOFF {handoff_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="File-backed multi-window competition coordinator")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="competition project root")
    parser.add_argument("--state-file", default=None, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("identify", help="bounded project identity check")
    init = sub.add_parser("init", help="create an empty state file if absent")
    init.add_argument("--force", action="store_true", help="replace an existing state file")
    status = sub.add_parser("status", help="print concise state")
    status.add_argument("--json", action="store_true", help="print machine-readable state")

    register = sub.add_parser("register", help="register a window and acquire its lock")
    register.add_argument("--role", required=True)
    register.add_argument("--mode", required=True, choices=sorted(MODES))
    register.add_argument("--task", default="")
    register.add_argument("--window-id", default="")
    register.add_argument("--write-scope", default="")
    register.add_argument("--handoff-path", default="")
    register.add_argument("--reopen", action="store_true", help="MAIN_RESEARCH-authorized new supplement")

    update = sub.add_parser("update", help="update a registered window status")
    update.add_argument("--window-id", required=True)
    update.add_argument("--status", required=True)
    update.add_argument("--task", default="")

    handoff = sub.add_parser("handoff", help="write the required handoff and release locks")
    handoff.add_argument("--window-id", required=True)
    handoff.add_argument("--freeze", action="store_true")
    handoff.add_argument("--handoff-path", default="")
    handoff.add_argument("--files-created", default="")
    handoff.add_argument("--files-modified", default="")
    handoff.add_argument("--results", default="")
    handoff.add_argument("--can-main-research-use", default="NO")
    handoff.add_argument("--claim-boundary", default="")
    handoff.add_argument("--known-problems", default="")
    handoff.add_argument("--next-action", default="")
    handoff.add_argument("--force", action="store_true")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    path = state_path(root, args.state_file)
    try:
        if args.command == "identify":
            return cmd_identify(root)
        if args.command == "init":
            return cmd_init(root, path, args.force)
        if args.command == "status":
            return cmd_status(root, path, args.json)
        if args.command == "register":
            return cmd_register(root, path, args)
        if args.command == "update":
            return cmd_update(root, path, args)
        if args.command == "handoff":
            return cmd_handoff(root, path, args)
        parser.error(f"unknown command {args.command}")
    except ManagerError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
