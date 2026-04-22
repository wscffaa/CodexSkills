#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_z(ts: dt.datetime | None = None) -> str:
    ts = ts or utc_now()
    return ts.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def project_root(path: str | None) -> Path:
    root = Path(path or os.getcwd()).expanduser().resolve()
    return root


def harness_root(root: Path) -> Path:
    return root / "docs" / "workflow" / "harness"


def tasks_path(root: Path) -> Path:
    return harness_root(root) / "tasks.json"


def progress_path(root: Path) -> Path:
    return harness_root(root) / "progress.log"


def active_path(root: Path) -> Path:
    return harness_root(root) / ".active"


def backup_path(root: Path) -> Path:
    return harness_root(root) / "tasks.json.bak"


def init_script_path(root: Path) -> Path:
    return harness_root(root) / "init.sh"


def ensure_dirs(root: Path) -> None:
    harness_root(root).mkdir(parents=True, exist_ok=True)


def default_state() -> dict[str, Any]:
    return {
        "version": 1,
        "created": iso_z(),
        "session_config": {
            "concurrency_mode": "exclusive",
            "max_tasks_per_session": 20,
            "max_sessions": 50,
        },
        "tasks": [],
        "session_count": 0,
        "last_session": None,
    }


def load_state(root: Path) -> dict[str, Any]:
    path = tasks_path(root)
    if not path.exists():
        raise FileNotFoundError(f"missing state file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("tasks.json must be an object")
    data.setdefault("tasks", [])
    data.setdefault("session_config", default_state()["session_config"])
    data.setdefault("session_count", 0)
    data.setdefault("last_session", None)
    return data


def save_state(root: Path, state: dict[str, Any]) -> None:
    ensure_dirs(root)
    current = tasks_path(root)
    tmp = current.with_suffix(".json.tmp")
    if current.exists():
        shutil.copy2(current, backup_path(root))
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, current)


def append_progress(root: Path, message: str) -> None:
    ensure_dirs(root)
    with progress_path(root).open("a", encoding="utf-8") as fh:
        fh.write(message.rstrip() + "\n")


def log(root: Path, session: int | str, kind: str, message: str) -> None:
    append_progress(root, f"[{iso_z()}] [SESSION-{session}] {kind} {message}")


def summarize_counts(state: dict[str, Any]) -> dict[str, int]:
    counts = {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0}
    for task in state.get("tasks", []):
        status = task.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    return counts


def next_task_id(state: dict[str, Any]) -> str:
    seen = {t.get("id", "") for t in state.get("tasks", [])}
    n = 1
    while True:
        candidate = f"task-{n:03d}"
        if candidate not in seen:
            return candidate
        n += 1


def normalize_priority(value: str | None) -> str:
    if not value:
        return "P1"
    value = value.strip().upper()
    return value if value in {"P0", "P1", "P2", "P3"} else "P1"


def parse_depends_on(raw: str | list[str] | None) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    text = str(raw).replace("|", ",").replace(";", ",")
    return [part.strip() for part in text.split(",") if part.strip()]


def task_template(
    task_id: str,
    title: str,
    description: str = "",
    acceptance_criteria: str = "",
    priority: str = "P1",
    depends_on: list[str] | None = None,
    validation_command: str | None = None,
    timeout_seconds: int = 300,
    max_attempts: int = 3,
    cse: bool = False,
    harness_engineering: bool = False,
    cleanup: str | None = None,
    rollback: bool = False,
) -> dict[str, Any]:
    return {
        "id": task_id,
        "title": title,
        "description": description,
        "acceptance_criteria": acceptance_criteria,
        "status": "pending",
        "priority": normalize_priority(priority),
        "depends_on": depends_on or [],
        "attempts": 0,
        "max_attempts": max_attempts,
        "started_at_commit": None,
        "validation": {
            "command": validation_command,
            "timeout_seconds": timeout_seconds,
        },
        "workflow": {
            "cse": cse,
            "harness_engineering": harness_engineering,
        },
        "on_failure": {
            "cleanup": cleanup,
            "rollback": rollback,
        },
        "error_log": [],
        "checkpoints": [],
        "completed_at": None,
    }


def lock_dir(root: Path) -> Path:
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    return Path("/tmp") / f"codex-harness-{digest}.lock"


class HarnessLock:
    def __init__(self, root: Path):
        self.path = lock_dir(root)

    def __enter__(self) -> "HarnessLock":
        deadline = time.time() + 5.0
        while True:
            try:
                self.path.mkdir(mode=0o700)
                (self.path / "pid").write_text(str(os.getpid()), encoding="utf-8")
                return self
            except FileExistsError:
                pid = self._read_pid()
                if pid is not None and self._pid_alive(pid):
                    if time.time() >= deadline:
                        raise TimeoutError(f"Another harness controller is active (pid={pid})")
                    time.sleep(0.05)
                    continue
                stale = self.path.with_name(f"{self.path.name}.stale.{os.getpid()}")
                try:
                    self.path.rename(stale)
                except Exception:
                    if time.time() >= deadline:
                        raise TimeoutError("Harness lock contention")
                    time.sleep(0.05)
                    continue
                shutil.rmtree(stale, ignore_errors=True)

    def __exit__(self, exc_type, exc, tb) -> None:
        shutil.rmtree(self.path, ignore_errors=True)

    def _read_pid(self) -> int | None:
        try:
            return int((self.path / "pid").read_text("utf-8").strip())
        except Exception:
            return None

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False


def git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def in_git_repo(root: Path) -> bool:
    return git_head(root) is not None


def run_shell(root: Path, command: str, timeout_seconds: int) -> tuple[int, str]:
    proc = subprocess.run(
        ["/bin/zsh", "-lc", command],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output.strip()


def cleanup_on_failure(root: Path, task: dict[str, Any], session: int) -> None:
    cleanup = task.get("on_failure", {}).get("cleanup")
    if cleanup:
        rc, out = run_shell(root, cleanup, 120)
        log(root, session, "CLEANUP", f"[{task['id']}] rc={rc} {cleanup}")
        if out:
            append_progress(root, out)


def maybe_rollback(root: Path, task: dict[str, Any], session: int, force: bool) -> None:
    if not in_git_repo(root):
        return
    if not force and not task.get("on_failure", {}).get("rollback", False):
        return
    base = task.get("started_at_commit")
    if not base:
        return
    rc1, _ = run_shell(root, f"git reset --hard {shlex.quote(base)}", 120)
    rc2, _ = run_shell(root, "git clean -fd", 120)
    log(root, session, "ROLLBACK", f"[{task['id']}] reset={rc1} clean={rc2} base={base}")


def checkpoint(task: dict[str, Any], step: int, total: int, description: str, root: Path, session: int) -> None:
    task.setdefault("checkpoints", []).append(
        {
            "step": step,
            "total": total,
            "description": description,
            "timestamp": iso_z(),
        }
    )
    log(root, session, "CHECKPOINT", f"[{task['id']}] step={step}/{total} {description}")


def dependency_failures(state: dict[str, Any]) -> None:
    by_id = {task.get("id"): task for task in state.get("tasks", [])}
    changed = True
    while changed:
        changed = False
        for task in state.get("tasks", []):
            if task.get("status") == "completed":
                continue
            for dep in task.get("depends_on", []):
                dep_task = by_id.get(dep)
                if not dep_task:
                    continue
                dep_failed = dep_task.get("status") == "failed"
                dep_exhausted = dep_task.get("attempts", 0) >= dep_task.get("max_attempts", 3)
                if dep_failed and dep_exhausted and task.get("status") != "failed":
                    task["status"] = "failed"
                    task.setdefault("error_log", []).append(f"[DEPENDENCY] Blocked by failed {dep}")
                    changed = True


def cycle_check(state: dict[str, Any]) -> None:
    by_id = {task.get("id"): task for task in state.get("tasks", [])}
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(task_id: str, chain: list[str]) -> None:
        if task_id in visited:
            return
        if task_id in visiting:
            node = by_id.get(task_id)
            if node is not None and node.get("status") != "failed":
                node["status"] = "failed"
                node.setdefault("error_log", []).append(
                    f"[DEPENDENCY] Circular dependency detected: {' -> '.join(chain + [task_id])}"
                )
            return
        visiting.add(task_id)
        task = by_id.get(task_id)
        if task is not None:
            for dep in task.get("depends_on", []):
                dfs(dep, chain + [task_id])
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        dfs(task_id, [])


def next_task(state: dict[str, Any]) -> dict[str, Any] | None:
    cycle_check(state)
    dependency_failures(state)
    completed = {t["id"] for t in state.get("tasks", []) if t.get("status") == "completed"}
    eligible: list[dict[str, Any]] = []
    for task in state.get("tasks", []):
        status = task.get("status")
        deps = task.get("depends_on", [])
        if any(dep not in completed for dep in deps):
            continue
        if status == "pending":
            eligible.append(task)
        elif status == "failed" and task.get("attempts", 0) < task.get("max_attempts", 3):
            eligible.append(task)
    if not eligible:
        return None
    eligible.sort(key=lambda t: (t.get("priority", "P9"), t.get("id", "")))
    return eligible[0]


def recover_interrupted(state: dict[str, Any], root: Path, session: int) -> None:
    for task in state.get("tasks", []):
        if task.get("status") != "in_progress":
            continue
        task["status"] = "failed"
        task.setdefault("error_log", []).append("[RECOVERY] Interrupted previous session; retry from task boundary")
        log(root, session, "RECOVERY", f"[{task['id']}] reset to failed for retry")


def build_prompt(task: dict[str, Any]) -> str:
    lines: list[str] = []
    workflow = task.get("workflow", {})
    if workflow.get("cse"):
        lines.append("$cybernetic-systems-engineering")
    if workflow.get("harness_engineering"):
        lines.append("Use harness-engineering because the execution or verification loop is weak.")
    lines.extend(
        [
            "This task is being executed under Codex harness.",
            f"Task ID: {task['id']}",
            f"Title: {task['title']}",
        ]
    )
    if task.get("description"):
        lines.append(f"Description: {task['description']}")
    if task.get("acceptance_criteria"):
        lines.append(f"Acceptance criteria: {task['acceptance_criteria']}")
    lines.extend(
        [
            "Constraints:",
            "- Make only the bounded changes required for this task.",
            "- Do not expand scope beyond the stated acceptance criteria.",
            "- Do not claim completion unless the validation command can pass after your changes.",
            "- Finish with changed files, validation status, and residual risks.",
        ]
    )
    return "\n".join(lines)


def run_codex_task(root: Path, task: dict[str, Any], session: int) -> tuple[int, str]:
    prompt = build_prompt(task)
    cmd = ["/opt/homebrew/bin/codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-C", str(root)]
    if not in_git_repo(root):
        cmd.append("--skip-git-repo-check")
    cmd.append(prompt)
    checkpoint(task, 1, 3, "dispatching codex exec", root, session)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, check=False)
    output = (proc.stdout or "") + (proc.stderr or "")
    if output.strip():
        append_progress(root, output.strip())
    checkpoint(task, 2, 3, f"codex exec rc={proc.returncode}", root, session)
    return proc.returncode, output


def validate_task(root: Path, task: dict[str, Any], session: int) -> tuple[bool, str]:
    validation = task.get("validation", {})
    command = validation.get("command")
    if not command:
        return False, "Missing validation.command"
    timeout_seconds = int(validation.get("timeout_seconds", 300))
    rc, out = run_shell(root, command, timeout_seconds)
    checkpoint(task, 3, 3, f"validation rc={rc}", root, session)
    if out:
        append_progress(root, out)
    return rc == 0, out


def cmd_init(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    ensure_dirs(root)
    if not tasks_path(root).exists():
        save_state(root, default_state())
    if not progress_path(root).exists():
        progress_path(root).write_text("", encoding="utf-8")
    active_path(root).touch()
    if args.with_init_template and not init_script_path(root).exists():
        init_script_path(root).write_text("#!/usr/bin/env bash\nset -euo pipefail\n# Idempotent project bootstrap here.\n", encoding="utf-8")
        init_script_path(root).chmod(0o755)
    append_progress(root, f"[{iso_z()}] [SESSION-0] INIT Harness initialized for {root}")
    print(f"Initialized harness at {harness_root(root)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = load_state(root)
    counts = summarize_counts(state)
    print(f"root: {root}")
    print(f"state: {tasks_path(root)}")
    print(f"active: {active_path(root).exists()}")
    print(
        "tasks:",
        f"pending={counts.get('pending', 0)}",
        f"in_progress={counts.get('in_progress', 0)}",
        f"completed={counts.get('completed', 0)}",
        f"failed={counts.get('failed', 0)}",
    )
    print(f"sessions: {state.get('session_count', 0)}")
    if progress_path(root).exists():
        tail = progress_path(root).read_text(encoding="utf-8").splitlines()[-5:]
        if tail:
            print("recent:")
            for line in tail:
                print(line)
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    with HarnessLock(root):
        state = load_state(root)
        task = task_template(
            task_id=next_task_id(state),
            title=args.title,
            description=args.description or "",
            acceptance_criteria=args.acceptance_criteria or "",
            priority=args.priority,
            depends_on=parse_depends_on(args.depends_on),
            validation_command=args.validation_command,
            timeout_seconds=args.timeout_seconds,
            max_attempts=args.max_attempts,
            cse=args.cse,
            harness_engineering=args.harness_engineering,
            cleanup=args.cleanup,
            rollback=args.rollback_on_failure,
        )
        state["tasks"].append(task)
        save_state(root, state)
        append_progress(root, f"[{iso_z()}] [SESSION-0] ADD [{task['id']}] {task['title']}")
    print(f"Added {task['id']}: {task['title']}")
    return 0


def import_row_task(state: dict[str, Any], row: dict[str, str]) -> dict[str, Any]:
    task_id = (row.get("id") or "").strip() or next_task_id(state)
    title = (row.get("title") or row.get("task") or row.get("summary") or "").strip()
    if not title:
        raise ValueError("CSV row missing title/task/summary")
    task = task_template(
        task_id=task_id,
        title=title,
        description=(row.get("description") or row.get("details") or "").strip(),
        acceptance_criteria=(row.get("acceptance_criteria") or row.get("acceptance") or "").strip(),
        priority=row.get("priority") or "P1",
        depends_on=parse_depends_on(row.get("depends_on")),
        validation_command=(row.get("validation_command") or row.get("validation") or "").strip() or None,
        timeout_seconds=int((row.get("timeout_seconds") or row.get("timeout") or 300)),
        max_attempts=int((row.get("max_attempts") or 3)),
        cse=(row.get("cse", "").strip().lower() in {"1", "true", "yes", "y"}),
        harness_engineering=(row.get("harness_engineering", "").strip().lower() in {"1", "true", "yes", "y"}),
        cleanup=(row.get("cleanup") or "").strip() or None,
        rollback=(row.get("rollback_on_failure", "").strip().lower() in {"1", "true", "yes", "y"}),
    )
    return task


def cmd_import_csv(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    csv_path = Path(args.csv_path).expanduser().resolve()
    with HarnessLock(root):
        state = load_state(root)
        with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            imported = 0
            for row in reader:
                if not any((value or "").strip() for value in row.values()):
                    continue
                task = import_row_task(state, row)
                state["tasks"].append(task)
                imported += 1
        save_state(root, state)
        append_progress(root, f"[{iso_z()}] [SESSION-0] IMPORT csv={csv_path} count={imported}")
    print(f"Imported {imported} tasks from {csv_path}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    with HarnessLock(root):
        state = load_state(root)
        state["session_count"] = int(state.get("session_count", 0)) + 1
        session = state["session_count"]
        max_sessions = int(state.get("session_config", {}).get("max_sessions", 50))
        if session > max_sessions:
            save_state(root, state)
            print("max_sessions reached")
            return 0
        recover_interrupted(state, root, session)
        save_state(root, state)
        log(root, session, "LOCK", f"acquired pid={os.getpid()}")
        ran = 0
        max_tasks = args.max_tasks or int(state.get("session_config", {}).get("max_tasks_per_session", 20))
        while ran < max_tasks:
            state = load_state(root)
            task = next_task(state)
            if task is None:
                counts = summarize_counts(state)
                log(
                    root,
                    session,
                    "STATS",
                    f"tasks_total={len(state.get('tasks', []))} completed={counts.get('completed', 0)} failed={counts.get('failed', 0)} pending={counts.get('pending', 0)}",
                )
                state["last_session"] = iso_z()
                save_state(root, state)
                print("No eligible tasks remain.")
                return 0
            task["status"] = "in_progress"
            task["started_at_commit"] = git_head(root)
            save_state(root, state)
            log(root, session, "START", f"[{task['id']}] {task['title']} base={task.get('started_at_commit')}")
            ran += 1
            exec_rc, _ = run_codex_task(root, task, session)
            if exec_rc != 0:
                task["status"] = "failed"
                task["attempts"] = int(task.get("attempts", 0)) + 1
                task.setdefault("error_log", []).append(f"[TASK_EXEC] codex exec failed rc={exec_rc}")
                cleanup_on_failure(root, task, session)
                maybe_rollback(root, task, session, args.rollback_on_failure)
                save_state(root, state)
                log(root, session, "ERROR", f"[{task['id']}] [TASK_EXEC] rc={exec_rc}")
                continue
            ok, validation_output = validate_task(root, task, session)
            if ok:
                task["status"] = "completed"
                task["completed_at"] = iso_z()
                save_state(root, state)
                log(root, session, "DONE", f"[{task['id']}] {task['title']}")
            else:
                task["status"] = "failed"
                task["attempts"] = int(task.get("attempts", 0)) + 1
                task.setdefault("error_log", []).append(f"[VALIDATION] {validation_output or 'validation failed'}")
                cleanup_on_failure(root, task, session)
                maybe_rollback(root, task, session, args.rollback_on_failure)
                save_state(root, state)
                log(root, session, "ERROR", f"[{task['id']}] [VALIDATION] failed")
        state = load_state(root)
        state["last_session"] = iso_z()
        save_state(root, state)
        log(root, session, "STATS", f"session_limit_reached max_tasks={max_tasks}")
        print(f"Stopped after {ran} task(s).")
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex-native harness controller")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize harness state")
    init.add_argument("project", nargs="?", default=".")
    init.add_argument("--with-init-template", action="store_true")
    init.set_defaults(func=cmd_init)

    status = sub.add_parser("status", help="Show harness state summary")
    status.add_argument("project", nargs="?", default=".")
    status.set_defaults(func=cmd_status)

    add = sub.add_parser("add", help="Add a new task")
    add.add_argument("project")
    add.add_argument("title")
    add.add_argument("--description")
    add.add_argument("--acceptance-criteria")
    add.add_argument("--priority", default="P1")
    add.add_argument("--depends-on")
    add.add_argument("--validation-command")
    add.add_argument("--timeout-seconds", type=int, default=300)
    add.add_argument("--max-attempts", type=int, default=3)
    add.add_argument("--cse", action="store_true")
    add.add_argument("--harness-engineering", action="store_true")
    add.add_argument("--cleanup")
    add.add_argument("--rollback-on-failure", action="store_true")
    add.set_defaults(func=cmd_add)

    import_csv = sub.add_parser("import-csv", help="Import tasks from CSV")
    import_csv.add_argument("project")
    import_csv.add_argument("csv_path")
    import_csv.set_defaults(func=cmd_import_csv)

    run = sub.add_parser("run", help="Run eligible harness tasks")
    run.add_argument("project", nargs="?", default=".")
    run.add_argument("--max-tasks", type=int)
    run.add_argument("--rollback-on-failure", action="store_true")
    run.set_defaults(func=cmd_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except TimeoutError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
